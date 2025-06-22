import streamlit as st
import matplotlib.pyplot as plt

st.title('Simulação Epidemiológica - Modelo SIR')

N = st.number_input('População Total', 100, 1000, 100)
I0 = st.number_input('Infectados', 1, 100, 1)
R0 = 0
beta = st.slider('Taxa de Transmissão (β)', 0.1, 1.0, 0.3, 0.01)
gamma = st.slider('Taxa de Recuperação (γ)', 0.05, 1.0, 0.1, 0.01)
days = st.slider('Dias de simulação', 1, 365, 180)
