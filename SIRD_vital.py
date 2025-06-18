import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import io
import pandas as pd


#st.set_page_config(page_title='Modelo SIRD - Dinâmica Vital', layout='wide')

def executar_sird_vital():
    st.title('Simulação SIRD - Dinâmica Vital')

    with st.sidebar:
        st.header('População Inicial')
        N = st.number_input('População Total (N)', 100, 1000000000, 5000)
        I0 = st.number_input('Infectados iniciais (I0)', 1, 10000, 1) # Infectados iniciais
        S0 = N - I0  # Suscetíveis iniciais
        R0 = 0 # Recuperados iniciais
        D0 = 0  # Mortos iniciais

        st.header('Parâmetros do Modelo')
        beta = st.slider('Taxa de transmissão (β)', 0.0, 1.0, 0.3, 0.01)
        gamma = st.slider('Taxa de recuperação (γ)', 0.0, 1.0, 0.1, 0.01)
        mu = st.slider('Taxa de natalidade/mortalidade natural(μ)', 0.0, 0.5, 0.01, 0.01)
        delta = st.slider('Taxa de mortalidade da doença (δ)', 0.0, 0.5, 0.01, 0.01)
        dias = st.slider('Dias de simulação', 1, 360, 160, 1)

        st.subheader('Curvas exibidas:')
        mostrar_S = st.checkbox('Susceptíveis', value=True)
        mostrar_I = st.checkbox('Infectados', value=True)
        mostrar_R = st.checkbox('Recuperados', value=True)
        mostrar_D = st.checkbox('Falecidos', value=True)

    # Condições iniciais
    N0 = S0 + I0 + R0

    y0 = [S0, I0, R0, D0]

    # Intervalo de tempo (dias)
    t = np.linspace(0, dias, dias)

    # Equações diferenciais do modelo
    def modelo_sird_vital(y, t, beta, gamma, mu, delta):
        S, I, R, D = y
        N = S + I + R  # população viva
        dSdt = mu * N - beta * S * I / N - mu * S
        dIdt = beta * S * I / N - gamma * I - mu * I - delta * I
        dRdt = gamma * I - mu * R
        dDdt = delta * I
        return [dSdt, dIdt, dRdt, dDdt]

    # Resolver o sistema
    resultado = odeint(modelo_sird_vital, y0, t, args=(beta, gamma, mu, delta))
    S, I, R, D = resultado.T

    fig, ax = plt.subplots(figsize=(10, 6))
    if mostrar_S:
        ax.plot(t, S, 'b', label='Suscetíveis')
    if mostrar_I:
        ax.plot(t, I, 'r', label='Infectados')
    if mostrar_R:
        ax.plot(t, R, 'g', label='Recuperados')
    if mostrar_D:
        ax.plot(t, D, 'y', label='Falecidos')

    ax.set_title('Evolução da Epidemia - Modelo SIRD com Dinâmica Vital')
    ax.set_xlabel('Dias')
    ax.set_ylabel('Número de Indivíduos')
    ax.legend()
    ax.grid(True)

    # Exibição do gráfico no Streamlit
    st.pyplot(fig)

    # --- Botão para salvar o gráfico como PNG ---
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    st.download_button(
        label="📊",
        data=buf.getvalue(),
        file_name="grafico_epidemia.png",
        mime="image/png"
    )
    # --- Botão para salvar os dados como CSV ---
    df_dados = pd.DataFrame({
        'Dia': t,
        'Susceptíveis': S,
        'Infectados': I,
        'Recuperados': R,
        'Falecidos': D
    })

    csv_data = df_dados.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄",
        data=csv_data,
        file_name="dados_epidemia.csv",
        mime="text/csv"
    )

    # Valores finais de cada variável
    st.subheader('Valores finais ao término da simulação:')
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Suscetíveis finais (S)', value=f'{int(S[-1])}',
                delta=f'{int(S[-1] - S0)}')

    with col2:
        st.metric('Infectados finais (I)', value=f'{int(I[-1])}',
                delta=f'{int(I[-1] - I0)}')

    with col3:
        st.metric('Recuperados finais (R)', value=f'{int(R[-1])}',
                delta=f'{int(R[-1] - R0)}')

    with col4:
        st.metric('Falecidos finais (D)', value=f'{int(D[-1])}',
                delta=f'{int(D[-1] - D0)}')

    # Adicionando um pequeno espaço
    st.write('')

    # Mostrando os valores percentuais finais
    st.subheader('Distribuição final da população (%):')
    total_final = S[-1] + I[-1] + R[-1] + D[-1]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('% Suscetíveis', value=f'{(S[-1]/total_final)*100:.2f}%')

    with col2:
        st.metric('% Infectados', value=f'{(I[-1]/total_final)*100:.2f}%')

    with col3:
        st.metric('% Recuperados', value=f'{(R[-1]/total_final)*100:.2f}%')

    with col4:
        st.metric('% Falecidos', value=f'{(D[-1]/total_final)*100:.2f}%')