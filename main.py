import streamlit as st
from SIR import executar_sir
from SIRD import executar_sird
from SIRD_duplo import executar_sird_duplo

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

# Conteúdo do app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Interface inicial com dropdown
modelos = ['Selecione um modelo',
           'SIR',
           'SIRD',
           'SIRD - Dupla População Interagente',
           'SIRD - Dinâmica Vital']
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
        
    case 'SIR':
        executar_sir()

    case 'SIRD':
        executar_sird()

    case 'SIRD - Dupla População Interagente':
        executar_sird_duplo()

    case 'SIRD - Dinâmica Vital':
        executar_sird_duplo()