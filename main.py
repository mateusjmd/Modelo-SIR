import streamlit as st
from SIR import executar_sir
from SIRD import executar_sird
from SIRD_duplo import executar_sird_duplo
from SIRD_vital import executar_sird_vital


# Título geral
st.set_page_config(page_title='Modelos Epidemiológicos', initial_sidebar_state='expanded')
st.title('Simulador de Modelos Epidemiológicos')

# Configurações em CSS para estilização da página
page_bg_style = """
<style>
/* Centralizar o título */
h1 {
    text-align: center;
    font-weight: 700;
}

/* Header transparente */
[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);  /* mantém compatível com dark */
}

/* Sidebar com leve opacidade */
[data-testid="stSidebar"] {
    background-color: rgba(30,30,30,0.95);
}

/* Caixa principal com padding e background com gradiente suave */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0A0A0A 0%, #1A237E 100%);
    min-height: 100vh;
}

/* Conteúdo principal com padding */
[data-testid="stAppViewContainer"] > .main {
    padding: 2rem 4rem;
}
</style>
"""
st.markdown(page_bg_style, unsafe_allow_html=True)

# Interface inicial com dropdown
modelos = ['Selecione um modelo',
           'SIR',
           'SIRD',
           'SIRD - Dupla População Interagente (Simplificado)',
           'SIRD - Dinâmica Vital']
modelo_selecionado = st.selectbox('Escolha um modelo:', modelos)

# Oculta a interface até que um modelo seja selecionado
match modelo_selecionado:
    case 'Selecione um modelo':
        # Estrutura da interface inicial em duas colunas
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Desenvolvedores')
            st.markdown('[Giovani M. M. Nagano](https://github.com/giovaninagano5)')
            st.markdown('[Letícia N. S. Andrade](https://github.com/LeticiaNunesAndrade)')
            st.markdown('[Lília H. G. Pessoa](https://github.com/LiliaGavazza)')
            st.markdown('[Mateus J. Mendes](https://github.com/mateusjmd)')

        with col2:
            st.subheader('Orientadores')
            st.markdown('[Daniel R. Cassar](https://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4262774J5)')
            st.markdown('[James M. Almeida](https://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4710448J1)')
            st.markdown('[Leandro N. Lemos](https://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4278041J7)')
            st.markdown('[Vinícius F. Wasques](https://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4355089T5)')
    
    case 'SIR':
        # Executa o modelo SIR
        executar_sir()

    case 'SIRD':
        # Executa o modelo SIRD
        executar_sird()

    case 'SIRD - Dupla População Interagente (Simplificado)':
        # Executa o modelo SIRD de dupla população interagente
        executar_sird_duplo()

    case 'SIRD - Dinâmica Vital':
        # Executa o modelo SIRD de dinâmica vital
        executar_sird_vital()
