import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import io
import pandas as pd


# A configuração da página deve estar logo no início
#st.set_page_config(page_title="Modelo SIR - Duas Populações", layout="wide")

def executar_sird_duplo():
    # Título
    st.title("Simulação SIR com Mortalidade - Duas Populações Interagentes")

    # Sidebar para entrada de parâmetros
    with st.sidebar:
        st.header("Parâmetros População A")
        N_A = st.number_input("População Total A", 100, 1000000, 5000)
        I0_A = st.number_input("Infectados Iniciais A", 0, N_A, 10)
        beta_A = st.slider("β A (transmissão)", 0.0, 1.0, 0.3, 0.01)
        gamma_A = st.slider("γ A (recuperação)", 0.0, 1.0, 0.1, 0.01)
        mi_A = st.slider("μ A (mortalidade)", 0.0, 0.5, 0.01, 0.01)

        st.header("Parâmetros População B")
        N_B = st.number_input("População Total B", 100, 1000000, 5000)
        I0_B = st.number_input("Infectados Iniciais B", 0, N_B, 10)
        beta_B = st.slider("β B (transmissão)", 0.0, 1.0, 0.3, 0.01)
        gamma_B = st.slider("γ B (recuperação)", 0.0, 1.0, 0.1, 0.01)
        mi_B = st.slider("μ B (mortalidade)", 0.0, 0.5, 0.01, 0.01)

        st.header("Interação e Duração")
        k_AB = st.slider("Fator de Transmissão de A → B", 0.0, 1.0, 0.05, 0.01)
        k_BA = st.slider("Fator de Transmissão de B → A", 0.0, 1.0, 0.05, 0.01)
        dias = st.slider("Dias de simulação", 1, 365, 160)

    # Condições iniciais
    S0_A = N_A - I0_A
    R0_A = 0
    D0_A = 0

    S0_B = N_B - I0_B
    R0_B = 0
    D0_B = 0

    v_inicial = [S0_A, I0_A, R0_A, D0_A, S0_B, I0_B, R0_B, D0_B]
    t = np.linspace(0, dias, dias)

    # Modelo com duas populações
    def modelo_sir_duas_pop(v, t):
        S_A, I_A, R_A, D_A, S_B, I_B, R_B, D_B = v

        dotS_A = -beta_A * S_A * I_A / N_A - k_BA * S_A * I_B / N_B
        dotI_A = beta_A * S_A * I_A / N_A + k_BA * S_A * I_B / N_B - gamma_A * I_A - mi_A * I_A
        dotR_A = gamma_A * I_A
        dotD_A = mi_A * I_A

        dotS_B = -beta_B * S_B * I_B / N_B - k_AB * S_B * I_A / N_A
        dotI_B = beta_B * S_B * I_B / N_B + k_AB * S_B * I_A / N_A - gamma_B * I_B - mi_B * I_B
        dotR_B = gamma_B * I_B
        dotD_B = mi_B * I_B

        return [dotS_A, dotI_A, dotR_A, dotD_A, dotS_B, dotI_B, dotR_B, dotD_B]

    # Integração numérica
    resultado = odeint(modelo_sir_duas_pop, v_inicial, t)
    S_A, I_A, R_A, D_A, S_B, I_B, R_B, D_B = resultado.T

    # Cálculo dos R0
    R0_A_val = beta_A / (gamma_A + mi_A) if (gamma_A + mi_A) > 0 else 0
    R0_B_val = beta_B / (gamma_B + mi_B) if (gamma_B + mi_B) > 0 else 0

    st.subheader(f"Número básico de reprodução")
    st.markdown(f"**População A**: R₀ = {R0_A_val:.2f} &nbsp;&nbsp;&nbsp;&nbsp; **População B**: R₀ = {R0_B_val:.2f}")

    # Gráficos
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(t, I_A, 'r', label='Infectados A')
    ax.plot(t, I_B, 'm', label='Infectados B')
    ax.plot(t, R_A, 'g', label='Recuperados A')
    ax.plot(t, R_B, 'c', label='Recuperados B')
    ax.plot(t, D_A, 'k', label='Falecidos A')
    ax.plot(t, D_B, 'y', label='Falecidos B')

    ax.set_title('Evolução da Epidemia - Duas Populações Interagentes')
    ax.set_xlabel('Dias')
    ax.set_ylabel('Número de Indivíduos')
    ax.grid(True)
    ax.legend()
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
        'Susceptíveis A': S_A,
        'Infectados A': I_A,
        'Recuperados A': R_A,
        'Falecidos A': D_A,
        'Susceptíveis B': S_B,
        'Infectados B': I_B,
        'Recuperados B': R_B,
        'Falecidos B': D_B,
    })

    csv_data = df_dados.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄",
        data=csv_data,
        file_name="dados_epidemia.csv",
        mime="text/csv"
    )


    # Valores finais
    st.subheader("Valores finais ao fim da simulação")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### População A")
        st.metric("Suscetíveis", int(S_A[-1]))
        st.metric("Infectados", int(I_A[-1]))
        st.metric("Recuperados", int(R_A[-1]))
        st.metric("Falecidos", int(D_A[-1]))

    with col2:
        st.markdown("### População B")
        st.metric("Suscetíveis", int(S_B[-1]))
        st.metric("Infectados", int(I_B[-1]))
        st.metric("Recuperados", int(R_B[-1]))
        st.metric("Falecidos", int(D_B[-1]))
