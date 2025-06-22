import numpy as np
import pandas as pd
from scipy.integrate import odeint
import streamlit as st
import matplotlib.pyplot as plt
import io


def executar_sird():
    """"
    Executa o modelo epidemiológico SIRD clássico quando chamada no main
    """

    st.header('Simulação - Modelo SIRD')

    # Exibe a barra lateral e os seus elementos
    with st.sidebar:
        st.header('População Inicial')
        N = st.number_input(f'População Total ($N$)', 1, 10_000_000_000, 10_000)
        I0 = st.number_input(f'Infectados iniciais ($I_0$)', 1, N, 100)
        S0 = N - I0 # Susceptíveis iniciais
        R0 = 0 # Recuperados iniciais
        D0 = 0 # mortos iniciais

        # Sliders para os parâmetros
        st.header('Parâmetros do Modelo')
        beta = st.slider(r'Taxa de transmissão ($\beta$)', 0.0, 1.0, 0.3, 0.01)
        gamma = st.slider(f'Taxa de recuperação ($\gamma$)', 0.0, 1.0, 0.1, 0.01)
        mu = st.slider(f'Taxa de mortalidade ($\mu$)', 0.0, 0.5, 0.01, 0.01)
        dias = st.slider('Dias de simulação', 1, 360, 160, 1)

        # Seleção das curvas exibidas no gráfico
        st.subheader('Curvas exibidas')
        mostrar_S = st.checkbox('Susceptíveis', value=True)
        mostrar_I = st.checkbox('Infectados', value=True)
        mostrar_R = st.checkbox('Recuperados', value=True)
        mostrar_D = st.checkbox('Mortos', value=True)
        
    # Período de simulação (dias)
    t = np.linspace(0, dias, dias)

    def modelo_sird(vetor, t):
        """
        Calcula as derivadas das variáveis do modelo epidemiológico SIRD

        Parâmetros:
        vetor: lista ou array contendo os valores atuais de [S, I, R, D] no tempo t
        t: tempo atual (passado automaticamente por odeint e não usado diretamente nessa função)

        Retorna:
        Lista com as derivadas correspondentes aos compartimentos:
        [dS/dt, dI/dt, dR/dt, dD/dt]
        """
        S, I, R, D = vetor

        # O número de susceptíveis reduz, por isso beta está negativo
        dS = -beta * S * I / N 
    
        # O primeiro termo calcula o número de novas infecções e o segundo, o número de recuperações
        # O termo (gamma * I) corresponde à recuperação dos infectados
        # O termo (mu * I) representa a redução de infectados devido a óbitos causados pela doença
        dI = beta * S * I / N - gamma * I - mu * I

        # O número de recuperados aumenta conforme os infectados se recuperam
        dR = gamma * I

        # O número de mortos aumenta proporcionalmente ao número de infectados (mu)
        dD = mu * I

        return np.array([dS, dI, dR, dD])

    # Condições iniciais
    vetor_inicial = [S0, I0, R0, D0]

    # Integra numericamente o sistema de equações diferenciais ao longo do período definido (t)
    resultado = odeint(modelo_sird, vetor_inicial, t)
    # Transoição matricial para a plotagem dos dados
    S, I, R, D = resultado.T

    # Cálculo e exibição do número básico de reprodução
    R0_basic = beta / (gamma + mu)
    st.write(f'Número básico de reprodução ($R_0$): {R0_basic:.2f}')


    # Plotagem das curvas selecionadas
    fig, ax = plt.subplots(figsize=(12, 6))
    if mostrar_S:
        ax.plot(t, S, 'b', label='Susceptíveis')
    if mostrar_I:
        ax.plot(t, I, 'r', label='Infectados')
    if mostrar_R:
        ax.plot(t, R, 'g', label='Recuperados')
    if mostrar_D:
        ax.plot(t, D, 'k', label='Mortos')

    # Configurações do gráfico
    ax.set_title('Evolução da Epidemia - Modelo SIR')
    ax.set_xlabel('Dias')
    ax.set_ylabel('Número de Indivíduos')
    ax.legend()
    ax.grid(True)
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
    col1, col2, col3, col4 = st.columns(4)

    total_final = S[-1] + I[-1] + R[-1] + D[-1]

    with col1:
        st.metric('susceptíveis finais (S)', value=f'{int(S[-1])}', delta=f'{int(S[-1] - S0)}')
        st.metric('% susceptíveis', value=f'{(S[-1]/total_final)*100:.2f}%')

    with col2:
        st.metric('Infectados finais (I)', value=f'{int(I[-1])}', delta=f'{int(I[-1] - I0)}')
        st.metric('% Infectados', value=f'{(I[-1]/total_final)*100:.2f}%')

    with col3:
        st.metric('Recuperados finais (R)', value=f'{int(R[-1])}', delta=f'{int(R[-1] - R0)}')
        st.metric('% Recuperados', value=f'{(R[-1]/total_final)*100:.2f}%')

    with col4:
        st.metric('Mortos finais (D)', value=f'{int(D[-1])}', delta=f'{int(D[-1] - D0)}')
        st.metric('% Mortos', value=f'{(D[-1]/total_final)*100:.2f}%')


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
