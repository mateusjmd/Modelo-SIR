import streamlit as st

#backgroundColor = "#801373"

page_bg_img = """
<style>
[data-testid='stAppViewContainer'] {
background-color: #801373
}

[data-testid='stHeader'] {
background-color: transparent;
}

html, body, [class*="css"] {
    color: white !important;
}
<style>
"""


# Conteúdo do app
st.markdown(page_bg_img, unsafe_allow_html=True)
#st.title("Dashboard")
#st.write("Este dashboard tem uma cor de fundo personalizada!")


# CSS para centralizar o título
centered_title = """
<style>
h1 {
    text-align: center;
}
</style>
"""

subheader = """
<style>
h1 {
    text-align: center;
}
</style>
"""
st.markdown(centered_title, unsafe_allow_html=True)
# Divisão em duas colunas
col1, col2 = st.columns(2,)

# Conteúdo da Coluna 1
with col1:
    st.subheader("Autores")
    st.write("Giovani M. Nagano")
    st.write("Letícia Nunes")
    st.write("Lília P. Gavazza")
    st.write("Mateus J. Mendes")
    # Você pode adicionar gráficos, tabelas, imagens, widgets, etc.

# Conteúdo da Coluna 2
with col2:
    st.subheader("Orientadores")
    st.write("Daniel Roberto Cassar")
    st.write("Leandro Lemos")
    st.write("James Almeida")
    st.write("Vinicius Francisco Wasquez")
    # Idem, sinta-se livre para customizar


