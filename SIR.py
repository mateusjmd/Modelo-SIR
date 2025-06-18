import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def executar_sir():
    # Exibe a interface do modelo SIR simples
    st.header('Simulação do Modelo SIR')

    with st.sidebar:
        N = st.number_input('População Total', 100, 10_000_000_000, 1000)
        I0 = st.number_input('Infectados iniciais', 1, 10_000_000_000, 1)
        R0 = 0
        S0 = N - I0 - R0
        beta = st.slider('Taxa de Transmissão (β)', 0.0, 1.0, 0.3, 0.01)
        gamma = st.slider('Taxa de Recuperação (γ)', 0.0, 1.0, 0.1, 0.01)
        dias = st.slider('Dias de simulação', 1, 365, 100)

        st.subheader('Curvas exibidas:')
        mostrar_S = st.checkbox('Susceptíveis', value=True)
        mostrar_I = st.checkbox('Infectados', value=True)
        mostrar_R = st.checkbox('Recuperados', value=True)

    t = np.linspace(0, dias, dias)

    def modelo_sir(vetor, t):
        S, I, R = vetor
        dS = -beta * S * I / N
        dI = beta * S * I / N - gamma * I
        dR = gamma * I
        return [dS, dI, dR]

    resultado = odeint(modelo_sir, [S0, I0, R0], t)
    S, I, R = resultado.T

    fig, ax = plt.subplots()
    if mostrar_S:
        ax.plot(t, S, 'b', label='Susceptíveis')
    if mostrar_I:
        ax.plot(t, I, 'r', label='Infectados')
    if mostrar_R:
        ax.plot(t, R, 'g', label='Recuperados')

    ax.set_title('Modelo SIR')
    ax.set_xlabel('Dias')
    ax.set_ylabel('População')
    ax.legend()
    st.pyplot(fig)