import streamlit as st
from SIR import executar_sir
from SIRD import executar_sird
from SIRD_duplo import executar_sird_duplo
from SIRD_vital import executar_sird_vital


# Título geral
st.set_page_config(page_title='Modelos Epidemiológicos')
st.title('Simulador de Modelos Epidemiológicos')

# Configurações em CSS para estilização da página
centered_title = """
<style>
h1 {
    text-align: center;
}
</style>
"""

page_bg_img = """
<style>
[data-testid='stHeader'] {
background-color: transparent;
}

<style>
h1 {
    text-align: center;
}
</style>
"""

# Ativa as alterações em CSS do dashboard
st.markdown(centered_title, unsafe_allow_html=True)
st.markdown(page_bg_img, unsafe_allow_html=True)

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
            st.markdown('[Giovani Massayuki Miranda Nagano](https://github.com/giovaninagano5)')
            st.markdown('[Letícia Nunes de Souza Andrade](https://github.com/LeticiaNunesAndrade)')
            st.markdown('[Lília Helena Gavazza Pessoa](https://github.com/LiliaGavazza)')
            st.markdown('[Mateus de Jesus Mendes](https://github.com/mateusjmd)')

        with col2:
            st.subheader('Orientadores')
            st.markdown('[Daniel Roberto Cassar](https://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4262774J5)')
            st.markdown('[James Moraes de Almeida](https://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4710448J1)')
            st.markdown('[Leandro Nascimento Lemos](https://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4278041J7)')
            st.markdown('[Vinícius Francisco Wasques](https://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4355089T5)')
    
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
