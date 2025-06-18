import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import streamlit as st
import io
import pandas as pd

def executar_sird():
    # Título da aplicação
    st.title('Simulação de Epidemia - Modelo SIR com Mortalidade')

    # Sidebar para os controles deslizantes
    with st.sidebar:
        st.header('População Inicial')
        N = st.number_input('População Total (N)', 100, 1000000000, 5000)
        I0 = st.number_input('Infectados iniciais (I0)', 1, 10000, 1) # Infectados iniciais
        S0 = N - I0  # Suscetíveis iniciais
        R0 = 0 # Recuperados iniciais
        D0 = 0  # Mortos iniciais

        st.header('Parâmetros do Modelo')
        
        # Sliders para os parâmetros
        beta = st.slider('Taxa de transmissão (β)', 0.0, 1.0, 0.3, 0.01)
        gamma = st.slider('Taxa de recuperação (γ)', 0.0, 1.0, 0.1, 0.01)
        mi = st.slider('Taxa de mortalidade (μ)', 0.0, 0.5, 0.01, 0.01)
        dias = st.slider('Dias de simulação', 1, 360, 160, 1)


        # Filtragem das curvas exibidas
        st.subheader('Curvas exibidas:')
        mostrar_S = st.checkbox('Susceptíveis', value=True)
        mostrar_I = st.checkbox('Infectados', value=True)
        mostrar_R = st.checkbox('Recuperados', value=True)
        mostrar_D = st.checkbox('Falecidos', value=True)
        
    # Período de tempo para simulação
    t = np.linspace(0, dias, dias)

    def modelo_sir(vetor, t):   
        S, I, R, D = vetor
        #Aqui definimos a função que fará os cálculos a partir dos dados imputados pelo usuário. O vetor de transmissão
        #é definido por três componentes, S, I e R respectivamente, que correspondem ao número de indivíduos sucetíveis a 
        #infecção (S), indivíduos infectados (I) e indivíduos recuperados, agora imunes à doença em questão (R)

        dotS = -beta * S * I / N
        #Aqui temos a primeira equação diferencial, em que se calcula a derivada de S em relação ao tempo, ou seja,
        #quantas pessoas deixam de ser sucetíveis a infecção ao longo do tempo, logo, a fórmula representa os novos 
        #infectados. Beta representa a taxa de transmissão, e , nessa equação, está negativo pois o número de sucetíveis
        #está diminuindo. N é a população total

        dotI = beta * S * I / N - gamma * I - mi * I # -> ADICIONAR COMENTÁRIOS SOBRE -mi * I
        #Aqui temos a segunda equação diferencial, em que se calcula a derivada de I, ou seja, como o número de
        #infectados muda com o tempo. O primeiro termo (beta * S * I / N) calcula o número de indivíduos sendo infectados.
        #Já o segundo termo (-gamma * I) calcula o número de pessoas se recuperando, ou seja, saindo do grupo dos 
        #infecados. Gamma é a taxa de recuperação.

        dotR = gamma * I
        #Aqui temos a terceira equação diferencial, em que se calcula a derivada de R, ou seja, quantas pessoas se
        #recuperam por unidade de tempo. Isso implica que R é proporcional a I.

        dotD = mi * I
        # ADICIONAR COMENTÁRIOS

        return np.array([dotS, dotI, dotR, dotD])

    # Condições iniciais
    v_inicial = [S0, I0, R0, D0]

    # Integração das equações
    resultado = odeint(modelo_sir, v_inicial, t)
    S, I, R, D = resultado.T

    # Cálculo do número básico de reprodução
    R0_basic = beta / (gamma + mi)
    st.subheader(f'Número básico de reprodução (R₀): {R0_basic:.2f}')

    # Plotagem do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    if mostrar_S:
        ax.plot(t, S, 'b', label='Susceptíveis')
    if mostrar_I:
        ax.plot(t, I, 'r', label='Infectados')
    if mostrar_R:
        ax.plot(t, R, 'g', label='Recuperados')
    if mostrar_D:
        ax.plot(t, D, 'y', label='Falecidos')


    ax.set_title('Evolução da Epidemia - Modelo SIR')
    ax.set_xlabel('Dias')
    ax.set_ylabel('Número de Indivíduos')
    ax.legend()
    ax.grid(True)

    # Exibição do gráfico no Streamlit
    st.pyplot(fig)

    # Botão para salvar o gráfico como PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    st.download_button(
        label="📊",
        data=buf.getvalue(),
        file_name="grafico_epidemia.png",
        mime="image/png"
    )
    # Botão para salvar os dados como CSV
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
        st.metric('Suscetíveis finais (S)', value=f'{int(S[-1])}', delta=f'{int(S[-1] - S0)}')

    with col2:
        st.metric('Infectados finais (I)', value=f'{int(I[-1])}', delta=f'{int(I[-1] - I0)}')

    with col3:
        st.metric('Recuperados finais (R)', value=f'{int(R[-1])}', delta=f'{int(R[-1] - R0)}')

    with col4:
        st.metric('Falecidos finais (D)', value=f'{int(D[-1])}', delta=f'{int(D[-1] - D0)}')

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