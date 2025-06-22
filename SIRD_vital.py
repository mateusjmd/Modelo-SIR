import numpy as np
import pandas as pd
from scipy.integrate import odeint
import streamlit as st
import matplotlib.pyplot as plt
import io


def executar_sird_vital():
    """"
    Executa o modelo epidemiológico SIRD de dinâmica vital quando chamada no main
    """
    st.header('Simulação SIRD - Dinâmica Vital')

    # Exibe a barra lateral e os seus elementos
    with st.sidebar:
        st.header('População Inicial')
        N = st.number_input(f'População Total ($N$)', 100, 10_000_000_000, 10_000)
        I0 = st.number_input(f'Infectados iniciais ($I_0$)', 1, N, 100)
        S0 = N - I0  # Suscetíveis iniciais
        R0 = 0 # Recuperados iniciais
        D0 = 0  # Mortos iniciais

        # Sliders para os parâmetros
        st.header('Parâmetros do Modelo')
        beta = st.slider(r'Taxa de transmissão ($\beta$)', 0.0, 1.0, 0.3, 0.01)
        gamma = st.slider(f'Taxa de recuperação ($\gamma$)', 0.0, 1.0, 0.1, 0.01)
        delta = st.slider('Taxa de natalidade/mortalidade natural(δ)', 0.0, 1.0, 0.01, 0.01)
        mu = st.slider(f'Taxa de mortalidade ($\mu$)', 0.0, 1.0, 0.01, 0.01)
        dias = st.slider('Dias de simulação', 1, 360, 160, 1)

        # Seleção das curvas exibidas no gráfico
        st.subheader('Curvas exibidas:')
        mostrar_S = st.checkbox('Susceptíveis', value=True)
        mostrar_I = st.checkbox('Infectados', value=True)
        mostrar_R = st.checkbox('Recuperados', value=True)
        mostrar_D = st.checkbox('Falecidos', value=True)

    vetor_inicial = [S0, I0, R0, D0]

    # Período de simulação (dias)
    t = np.linspace(0, dias, dias)

    def modelo_sird_vital(vetor, t):
        """
        Calcula as derivadas do modelo epidemiológico SIRD com dinâmica vital (natalidade e mortalidade natural)

        Parâmetros:
        vetor: lista ou array contendo os valores atuais de [S, I, R, D] no tempo t
        t: tempo atual (passado automaticamente por odeint e não usado diretamente nessa função)

        Retorna:
        Lista com as derivadas de cada compartimento:
        [dS/dt, dI/dt, dR/dt, dD/dt]
        """

        S, I, R, D = vetor

        # População viva, isto é, não inclui os mortos
        N = S + I + R 

        # Taxa de variação dos susceptíveis
        dS = mu * N - beta * S * I / N - mu * S
        # Natalidade: mu * N
        # Infecção: - beta * S * I / N
        # Mortalidade natural: - mu * S

        # Taxa de variação dos infectados
        dI = beta * S * I / N - gamma * I - mu * I - delta * I
        # Infecção: + beta * S * I / N
        # Recuperação: - gamma * I
        # Mortalidade natural: - mu * I
        # Mortalidade por doença: - delta * I
        
        # Taxa de variação dos recuperados
        dR = gamma * I - mu * R
        # Recuperação: + gamma * I
        # Mortalidade natural: - mu * R

        # Taxa de variação dos óbitos causados pela doença
        dD = delta * I

        return [dS, dI, dR, dD]

    # Integra numericamente o sistema de equações diferenciais ao longo do período definido (t)
    resultado = odeint(modelo_sird_vital, vetor_inicial, t)
    # Transposição matricial para a plotagem dos dados 
    S, I, R, D = resultado.T


    # Cálculo e exibição dos números básicos de reprodução
    R0_basic = beta / (gamma + mu)
    st.write(f'Número básico de reprodução ($R_0$): {R0_basic:.2f}')

    # Plotagem das curvas selecionadas
    fig, ax = plt.subplots(figsize=(12, 6))
    if mostrar_S:
        ax.plot(t, S, 'b', label='Suscetíveis')
    if mostrar_I:
        ax.plot(t, I, 'r', label='Infectados')
    if mostrar_R:
        ax.plot(t, R, 'g', label='Recuperados')
    if mostrar_D:
        ax.plot(t, D, 'y', label='Falecidos')

    # Configurações do gráfico
    ax.set_title('Evolução da Epidemia - Modelo SIRD com Dinâmica Vital')
    ax.set_xlabel('Dias')
    ax.set_ylabel('Número de Indivíduos')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

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
    st.subheader('Distribuição final da população:')
    col1, col2, col3, col4 = st.columns(4)
    total_final = S[-1] + I[-1] + R[-1] + D[-1]


    with col1:
        st.metric('Suscetíveis finais (S)', value=f'{int(S[-1])}', delta=f'{int(S[-1] - S0)}')
        st.metric('% Suscetíveis', value=f'{(S[-1]/total_final)*100:.2f}%')

    with col2:
        st.metric('Infectados finais (I)', value=f'{int(I[-1])}', delta=f'{int(I[-1] - I0)}')
        st.metric('% Infectados', value=f'{(I[-1]/total_final)*100:.2f}%')

    with col3:
        st.metric('Recuperados finais (R)', value=f'{int(R[-1])}', delta=f'{int(R[-1] - R0)}')
        st.metric('% Recuperados', value=f'{(R[-1]/total_final)*100:.2f}%')

    with col4:
        st.metric('Falecidos finais (D)', value=f'{int(D[-1])}', delta=f'{int(D[-1] - D0)}')
        st.metric('% Falecidos', value=f'{(D[-1]/total_final)*100:.2f}%')


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
