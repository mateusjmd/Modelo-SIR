import numpy as np
import pandas as pd
from scipy.integrate import odeint
import streamlit as st
import matplotlib.pyplot as plt
import io


def executar_sird_duplo():
    """"
    Executa o modelo epidemiológico SIRD de dupla população interagente quando chamada no main
    """
    st.header('Simulação SIRD - Dupla População Interagente')

    # Exibe a barra lateral e os seus elementos
    with st.sidebar:
        # O parâmetro key é usado porque o Streamlit não distingue widgets com configurações iguais
        
        # Parâmetros da população A
        st.header('Parâmetros da População A')
        N_A = st.number_input('População Total', 100, 10_000_000_000, 1000, key='N_A')
        I0_A = st.number_input('Infectados Iniciais', 1, N_A, 100, key='I0_A')
        beta_A = st.slider(r'Taxa de transmissão ($\beta$)', 0.0, 1.0, 0.3, 0.01, key='beta_A')
        gamma_A = st.slider(f'Taxa de recuperação ($\gamma$)', 0.0, 1.0, 0.1, 0.01, key='gamma_A')
        mu_A = st.slider(f'Taxa de mortalidade ($\mu$)', 0.0, 1.0, 0.01, 0.01, key='mu_A')

        # Parâmetros da população B
        st.header('Parâmetros da População B')
        N_B = st.number_input('População Total', 100, 1_000_000_000, 5000, key='N_B')
        I0_B = st.number_input('Infectados Iniciais', 0, N_B, 10, key='I0_B')
        beta_B = st.slider(r'Taxa de transmissão ($\beta$)', 0.0, 1.0, 0.3, 0.01, key='beta_B')
        gamma_B = st.slider(f'Taxa de recuperação ($\gamma$)', 0.0, 1.0, 0.1, 0.01, key='gamma_B')
        mu_B = st.slider(f'Taxa de mortalidade ($\mu$)', 0.0, 1.0, 0.01, 0.01, key='mu_B')

        # Parâmetros interpopulacionais e temporais
        st.header('Interação e Duração')
        k_AB = st.slider('Fator de Transmissão de A → B', 0.0, 1.0, 0.05, 0.01)
        k_BA = st.slider('Fator de Transmissão de B → A', 0.0, 1.0, 0.05, 0.01)
        dias = st.slider('Dias de simulação', 1, 365, 160)

        # Seleção das curvas exibidas no gráfico
        st.header('Curvas Exibidas')
        st.write('População A')
        mostrar_S_A = st.checkbox('Susceptíveis', value=True, key='mostrar_S_A')
        mostrar_I_A = st.checkbox('Infectados', value=True, key='mostrar_I_A')
        mostrar_R_A = st.checkbox('Recuperados', value=True, key='mostrar_R_A')
        mostrar_D_A = st.checkbox('Mortos', value=True, key='mostrar_D_A')

        st.write('População B')
        mostrar_S_B = st.checkbox('Susceptíveis', value=True, key='mostrar_S_B')
        mostrar_I_B = st.checkbox('Infectados', value=True, key='mostrar_I_B')
        mostrar_R_B = st.checkbox('Recuperados', value=True, key='mostrar_R_B')
        mostrar_D_B = st.checkbox('Mortos', value=True, key='mostrar_D_B')

    # Condições iniciais de cada população
    S0_A = N_A - I0_A
    R0_A = 0
    D0_A = 0

    S0_B = N_B - I0_B
    R0_B = 0
    D0_B = 0

    # Condições iniciais
    vetor_inicial = [S0_A, I0_A, R0_A, D0_A, S0_B, I0_B, R0_B, D0_B]

    # Período de simulação (dias)
    t = np.linspace(0, dias, dias)

    def modelo_sir_duplo(vetor, t):
        """
        Calcula as derivadas das variáveis do modelo epidemiológico SIRD acoplado a duas populações interagentes

        Parâmetros:
        vetor: lista ou array contendo os valores atuais dos compartimentos, na seguinte ordem:
        [S_A, I_A, R_A, D_A, S_B, I_B, R_B, D_B]

        t: tempo atual (passado automaticamente por odeint e não usado diretamente nessa função)

        Retorna:
        Uma lista com as derivadas correspondentes aos compartimentos:
        [dS_A/dt, dI_A/dt, dR_A/dt, dD_A/dt, dS_B/dt, dI_B/dt, dR_B/dt, dD_B/dt]
        """
        S_A, I_A, R_A, D_A, S_B, I_B, R_B, D_B = vetor

        # ----- POPULAÇÃO A -----
        # Taxa de variação dos suscetíveis de A
        dS_A = - beta_A * S_A * I_A / N_A - k_BA * S_A * I_B / N_B
        # Infecção interna: - beta_A * S_A * I_A / N_A
        # Infecção cruzada (de B para A): - k_BA * S_A * I_B / N_B

        # Taxa de variação dos infectados de A
        dI_A = beta_A * S_A * I_A / N_A + k_BA * S_A * I_B / N_B - gamma_A * I_A - mu_A * I_A
        # Infecção interna: + beta_A * S_A * I_A / N_A
        # Infecção cruzada: + k_BA * S_A * I_B / N_B
        # Recuperação: - gamma_A * I_A
        # Mortalidade da doença: - mu_A * I_A

        # Taxa de variação dos recuperados de A
        dR_A = gamma_A * I_A
        # Recuperação: + gamma_A * I_A

        # Taxa de variação dos óbitos de A
        dD_A = mu_A * I_A
        # Mortalidade da doença: + mu_A * I_A

        # ----- POPULAÇÃO B -----

        # Taxa de variação dos suscetíveis de B
        dS_B = - beta_B * S_B * I_B / N_B - k_AB * S_B * I_A / N_A
        # Infecção interna: - beta_B * S_B * I_B / N_B
        # Infecção cruzada (de A para B): - k_AB * S_B * I_A / N_A

        # Taxa de variação dos infectados de B
        dI_B = beta_B * S_B * I_B / N_B + k_AB * S_B * I_A / N_A - gamma_B * I_B - mu_B * I_B
        # Infecção interna: + beta_B * S_B * I_B / N_B
        # Infecção cruzada: + k_AB * S_B * I_A / N_A
        # Recuperação: - gamma_B * I_B
        # Mortalidade da doença: - mu_B * I_B

        # Taxa de variação dos recuperados de B
        dR_B = gamma_B * I_B
        # Recuperação: + gamma_B * I_B

        # Taxa de variação dos óbitos de B
        dD_B = mu_B * I_B
        # Mortalidade da doença: + mu_B * I_B

        return [dS_A, dI_A, dR_A, dD_A, dS_B, dI_B, dR_B, dD_B]

    # Integra numericamente o sistema de equações diferenciais ao longo do período definido (t)
    resultado = odeint(modelo_sir_duplo, vetor_inicial, t)
    # Transposição matricial para a plotagem dos dados
    S_A, I_A, R_A, D_A, S_B, I_B, R_B, D_B = resultado.T

    # Cálculo e exibição dos números básicos de reprodução
    R0_A_val = beta_A / (gamma_A + mu_A) if (gamma_A + mu_A) > 0 else 0
    R0_B_val = beta_B / (gamma_B + mu_B) if (gamma_B + mu_B) > 0 else 0
    st.subheader('Números básicos de reprodução:')
    st.markdown(f'- População A: $R_0$ = {R0_A_val:.2f}')
    st.markdown(f'- População B: $R_0$ = {R0_B_val:.2f}')

    # Plotagem das curvas selecionadas
    fig, ax = plt.subplots(figsize=(12, 6))
    if mostrar_S_A:
        ax.plot(t, S_A, 'b', label='Susceptíveis A')
    if mostrar_I_A:
        ax.plot(t, I_A, 'r', label='Infectados A')
    if mostrar_R_A:
        ax.plot(t, R_A, 'g', label='Recuperados A')
    if mostrar_D_A:
        ax.plot(t, D_A, 'k', label='Mortos A')

    if mostrar_S_B:
        ax.plot(t, S_B, 'b', label='Susceptíveis B', linestyle='dashed')
    if mostrar_I_B:
        ax.plot(t, I_B, 'r', label='Infectados B', linestyle='dashed')
    if mostrar_R_B:
        ax.plot(t, R_B, 'g', label='Recuperados B', linestyle='dashed')
    if mostrar_D_B:
        ax.plot(t, D_B, 'k', label='Mortos B', linestyle='dashed')
    
    # Configurações do gráfico
    ax.set_title('Evolução da Epidemia - Duas Populações Interagentes')
    ax.set_xlabel('Dias')
    ax.set_ylabel('Número de Indivíduos')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # Encontra o dia e o valor correspondente ao pico de infecções
    pico_A = t[np.argmax(I_A)]
    max_infeccoes_A = np.max(I_A)
    
    pico_B = t[np.argmax(I_B)]
    max_infeccoes_B = np.max(I_B)

    # Exibe os resultados dos picos
    st.subheader('Picos da Epidemia (Máximo de Infectados)')
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
    - **Dia do pico da população A:** {int(pico_A)}  
    - **Número máximo de infectados simultâneos da população A:** {int(max_infeccoes_A)}""")

    with col2:
        st.markdown(f"""
    - **Dia do pico da população B:** {int(pico_B)}  
    - **Número máximo de infectados simultâneos da população B:**: {int(max_infeccoes_B)}""")


    # Valores finais da cada variável
    st.subheader('Valores finais ao fim da simulação')
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### População A')
        st.metric('Suscetíveis', int(S_A[-1]))
        st.metric('Infectados', int(I_A[-1]))
        print(I_A)
        st.metric('Recuperados', int(R_A[-1]))
        st.metric('Mortos', int(D_A[-1]))

    with col2:
        st.markdown('### População B')
        st.metric('Suscetíveis', int(S_B[-1]))
        st.metric('Infectados', int(I_B[-1]))
        st.metric('Recuperados', int(R_B[-1]))
        st.metric('Mortos', int(D_B[-1]))


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
    #  Botão de download dos dados em CSV
    df_dados = pd.DataFrame({
        'Dia': t,
        'Susceptíveis A': S_A,
        'Infectados A': I_A,
        'Recuperados A': R_A,
        'Mortos A': D_A,
        'Susceptíveis B': S_B,
        'Infectados B': I_B,
        'Recuperados B': R_B,
        'Mortos B': D_B,
    })

    csv_data = df_dados.to_csv(index=False).encode('utf-8')
    st.download_button(
        label='📄 Download CSV',
        data=csv_data,
        file_name='dados_epidemia.csv',
        mime='text/csv'
    )
