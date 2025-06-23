import numpy as np
import pandas as pd
from scipy.integrate import odeint
import streamlit as st
import matplotlib.pyplot as plt
import io


def executar_sir():
    """"
    Executa o modelo epidemiológico SIR clássico quando chamada no main
    """

    st.header('Simulação - Modelo SIR')

    # Exibe a barra lateral e os seus elementos
    with st.sidebar:
        # Definição dos parâmetros
        N = st.number_input(f'População Total ($N$)', 100, 10_000_000_000, 10_000)
        I0 = st.number_input(f'Infectados iniciais ($I_0$)', 1, 10_000_000_000, 1)
        R0 = 0
        S0 = N - I0 - R0
        beta = st.slider(r'Taxa de Transmissão ($\beta$)', 0.0, 1.0, 0.3, 0.01)
        gamma = st.slider(f'Taxa de Recuperação ($\gamma$)', 0.0, 1.0, 0.1, 0.01)
        dias = st.slider('Dias de simulação', 1, 365, 100)

        # Seleção das curvas exibidas no gráfico
        st.subheader('Curvas exibidas:')
        mostrar_S = st.checkbox('Susceptíveis', value=True)
        mostrar_I = st.checkbox('Infectados', value=True)
        mostrar_R = st.checkbox('Recuperados', value=True)


    def modelo_sir(vetor, t):
        """
        Calcula as derivadas das variáveis do modelo epidemiológico SIR

        Parâmetros:
        vetor: lista ou array contendo os valores atuais de [S, I, R] no tempo t
        t: tempo atual (passado automaticamente por odeint e não usado diretamente nessa função)

        Retorna:
        Lista com as derivadas correspondentes aos compartimentos:
        [dS/dt, dI/dt, dR/dt, dD/dt]
        """

        S, I, R = vetor
        dS = -beta * S * I / N
        dI = beta * S * I / N - gamma * I
        dR = gamma * I
        return [dS, dI, dR]

    # Período de simulação (dias)
    t = np.linspace(0, dias, dias)

    # Integra numericamente o sistema de equações diferenciais ao longo do período definido (t)
    resultado = odeint(modelo_sir, [S0, I0, R0], t)
    # Transposição matricial para a plotagem dos dados
    S, I, R = resultado.T


    # Plotagem das curvas selecionadas
    fig, ax = plt.subplots(figsize=(12,6))
    if mostrar_S:
        ax.plot(t, S, 'b', label='Susceptíveis')
    if mostrar_I:
        ax.plot(t, I, 'r', label='Infectados')
    if mostrar_R:
        ax.plot(t, R, 'g', label='Recuperados')

    # Configurações do gráfico
    ax.set_title('Modelo SIR')
    ax.set_xlabel('Dias')
    ax.set_ylabel('Número de Indivíduos')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig) # Exibe o gráfico


    # Encontra o dia e o valor correspondente ao pico de infecções
    pico = t[np.argmax(I)]
    max_infeccoes = np.max(I)

    # Exibe os resultados dos picos
    st.subheader('Pico da Epidemia (Máximo de Infectados)')
    st.markdown(f"""
    - **Dia do pico**: {int(pico)}  
    - **Número máximo de infectados simultâneos**: {int(max_infeccoes)}  
    """)


    # Valores finais de cada variável
    st.subheader('Distribuição final da população')
    col1, col2, col3 = st.columns(3)

    total_final = S[-1] + I[-1] + R[-1]

    with col1:
        st.metric(f'Suscetíveis finais ($S$)', value=f'{int(S[-1])}', delta=f'{int(S[-1] - S0)}')
        st.metric('% Suscetíveis', value=f'{(S[-1]/total_final)*100:.2f}%')

    with col2:
        st.metric(f'Infectados finais ($I$)', value=f'{int(I[-1])}', delta=f'{int(I[-1] - I0)}')
        st.metric('% Infectados', value=f'{(I[-1]/total_final)*100:.2f}%')

    with col3:
        st.metric(f'Recuperados finais ($R$)', value=f'{int(R[-1])}', delta=f'{int(R[-1] - R0)}')
        st.metric('% Recuperados', value=f'{(R[-1]/total_final)*100:.2f}%')


    st.subheader('Download dos Dados')
    # Botão de download do gráfico em PNG
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    st.download_button(
        label='📊 Download Gráfico',
        data=buf.getvalue(),
        file_name='grafico_epidemia.png',
        mime='image/png'
    )

    # Botão de download dos dados em CSV
    df_dados = pd.DataFrame({
        'Dia': t,
        'Susceptíveis': S,
        'Infectados': I,
        'Recuperados': R,
    })

    csv_data = df_dados.to_csv(index=False).encode('utf-8')
    st.download_button(
        label='📄 Download CSV',
        data=csv_data,
        file_name='dados_epidemia.csv',
        mime='text/csv'
    )
