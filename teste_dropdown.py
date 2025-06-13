import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Título geral
st.set_page_config(page_title='Modelos Epidemiológicos')
st.title('Simulador de Modelos Epidemiológicos')

centered_title = '''
<style>
h1 {
    text-align: center;
}
</style>
'''
st.markdown(centered_title, unsafe_allow_html=True)

# Interface inicial com dropdown
modelos = ['Selecione um modelo', 'Modelo SIR', 'Modelo SIRD', 'Modelo SIRD Duplo', 'Dinâmica Vital']
modelo_selecionado = st.selectbox('Escolha um modelo:', modelos)

# Oculta a interface até que um modelo seja selecionado
match modelo_selecionado:
    case 'Selecione um modelo':

        # Divisão em duas colunas
        col1, col2 = st.columns(2)

        # Conteúdo da Coluna 1
        with col1:
            st.subheader('Autores')
            st.write('Giovani M. Nagano')
            st.write('Letícia Nunes')
            st.write('Lília Gavazza')
            st.write('Mateus J. Mendes')

        # Conteúdo da Coluna 2
        with col2:
            st.subheader('Orientadores')
            st.write('Daniel Roberto Cassar')
            st.write('Leandro Lemos')
            st.write('James Almeida')
            st.write('Vinicius Francisco Wasquez')
        
    case 'Modelo SIR':
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

    case 'Modelo SIRD': # ---------------------------------------------------------------------------
        st.header('Modelo SIRD')
        
            # Configuração da página
        #st.set_page_config(page_title='Modelo SIR de Epidemias', layout='wide')

        # Título da aplicação
        st.title('Simulação de Epidemia - Modelo SIR com Mortalidade')

        # Sidebar para os controles deslizantes
        with st.sidebar:
            st.header('População Inicial')
            N = st.number_input('População Total (N)', 100, 1000000000, 5000)
            I0 = st.number_input('Infectados iniciais (I0)', 1, 10000, 1) # Infectados iniciais
            S0 = N - I0  # Susceptíveis iniciais
            R0 = 0 # Recuperados iniciais
            D0 = 0  # Mortos iniciais

            st.header('Parâmetros do Modelo')
            
            # Sliders para os parâmetros
            beta = st.slider('Taxa de transmissão (β)', 0.0, 1.0, 0.3, 0.01)
            gamma = st.slider('Taxa de recuperação (γ)', 0.0, 1.0, 0.1, 0.01)
            mi = st.slider('Taxa de mortalidade (μ)', 0.0, 0.5, 0.01, 0.01)
            dias = st.slider('Dias de simulação', 1, 360, 160, 1)

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

        # Valores finais de cada variável
        st.subheader('Valores finais ao término da simulação:')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric('Susceptíveis finais (S)', value=f'{int(S[-1])}',
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
            st.metric('% Susceptíveis', value=f'{(S[-1]/total_final)*100:.2f}%')

        with col2:
            st.metric('% Infectados', value=f'{(I[-1]/total_final)*100:.2f}%')

        with col3:
            st.metric('% Recuperados', value=f'{(R[-1]/total_final)*100:.2f}%')

        with col4:
            st.metric('% Falecidos', value=f'{(D[-1]/total_final)*100:.2f}%')

    case 'Modelo SIRD Duplo': # ---------------------------------------------------------------------------
        st.header('Modelo SIRD Duplo')
        # A configuração da página deve estar logo no início
        #st.set_page_config(page_title='Modelo SIR - Duas Populações', layout='wide')

        # Título
        st.title('Simulação SIR com Mortalidade - Duas Populações Interagentes')

        # Sidebar para entrada de parâmetros
        with st.sidebar:
            st.header('Parâmetros População A')
            N_A = st.number_input('População Total A', 100, 1000000, 5000)
            I0_A = st.number_input('Infectados Iniciais A', 0, N_A, 10)
            beta_A = st.slider('β A (transmissão)', 0.0, 1.0, 0.3, 0.01)
            gamma_A = st.slider('γ A (recuperação)', 0.0, 1.0, 0.1, 0.01)
            mi_A = st.slider('μ A (mortalidade)', 0.0, 0.5, 0.01, 0.01)

            st.header('Parâmetros População B')
            N_B = st.number_input('População Total B', 100, 1000000, 5000)
            I0_B = st.number_input('Infectados Iniciais B', 0, N_B, 10)
            beta_B = st.slider('β B (transmissão)', 0.0, 1.0, 0.3, 0.01)
            gamma_B = st.slider('γ B (recuperação)', 0.0, 1.0, 0.1, 0.01)
            mi_B = st.slider('μ B (mortalidade)', 0.0, 0.5, 0.01, 0.01)

            st.header('Interação e Duração')
            k_AB = st.slider('Fator de Transmissão de A → B', 0.0, 1.0, 0.05, 0.01)
            k_BA = st.slider('Fator de Transmissão de B → A', 0.0, 1.0, 0.05, 0.01)
            dias = st.slider('Dias de simulação', 1, 365, 160)

            st.subheader('Curvas exibidas:')
            mostrar_S_A = st.checkbox('Susceptíveis A', value=True)
            mostrar_I_A = st.checkbox('Infectados A', value=True)
            mostrar_R_A = st.checkbox('Recuperados A ', value=True)
            mostrar_D_A = st.checkbox('Falecidos A', value=True)
            mostrar_S_B = st.checkbox('Susceptíveis B', value=True)
            mostrar_I_B = st.checkbox('Infectados B', value=True)
            mostrar_R_B = st.checkbox('Recuperados B', value=True)
            mostrar_D_B = st.checkbox('Falecidos B', value=True)

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

        st.subheader(f'Número básico de reprodução')
        st.markdown(f'**População A**: R₀ = {R0_A_val:.2f} &nbsp;&nbsp;&nbsp;&nbsp; **População B**: R₀ = {R0_B_val:.2f}')

        # Gráficos
        fig, ax = plt.subplots(figsize=(12, 6))

        if mostrar_S_A:
            ax.plot(t, S_A, 'b--', label='Suceptíveis A')
        if mostrar_I_A:
            ax.plot(t, I_A, 'r', label='Infectados A')
        if mostrar_R_A:
            ax.plot(t, R_A, 'g', label='Recuperados A')
        if mostrar_D_A:
            ax.plot(t, D_A, 'k', label='Falecidos A')


        if mostrar_S_B:
            ax.plot(t, S_B, 'c--', label='Suceptíveis B')
        if mostrar_I_B:
            ax.plot(t, I_B, 'm', label='Infectados B')
        if mostrar_R_B:
            ax.plot(t, R_B, 'c', label='Recuperados B')
        if mostrar_D_B:
            ax.plot(t, D_B, 'y', label='Falecidos B')

        ax.set_title('Evolução da Epidemia - Duas Populações Interagentes')
        ax.set_xlabel('Dias')
        ax.set_ylabel('Número de Indivíduos')
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        # Valores finais
        st.subheader('Valores finais ao fim da simulação')
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('### População A')
            st.metric('Susceptíveis', int(S_A[-1]))
            st.metric('Infectados', int(I_A[-1]))
            st.metric('Recuperados', int(R_A[-1]))
            st.metric('Falecidos', int(D_A[-1]))

        with col2:
            st.markdown('### População B')
            st.metric('Susceptíveis', int(S_B[-1]))
            st.metric('Infectados', int(I_B[-1]))
            st.metric('Recuperados', int(R_B[-1]))
            st.metric('Falecidos', int(D_B[-1]))

    case 'Dinâmica Vital': # ---------------------------------------------------------------------------
        st.header('Modelo de Dinâmica Vital')
        # Aqui colocaria a lógica do modelo com duas populações
