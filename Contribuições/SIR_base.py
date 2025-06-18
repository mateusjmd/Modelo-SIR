import numpy as np
from scipy.integrate import odeint

def executar_sir(): 
        N = int(input('População Total: '))
        I0 = int(input('Infectados iniciais: '))
        R0 = 0
        S0 = N - I0 - R0
        beta = float(input('Taxa de Transmissão (β): '))
        gamma = float(input('Taxa de Recuperação (γ): '))
        dias = int(input('Dias de simulação: '))

        t = np.linspace(0, dias, dias)

        def modelo_sir(vetor, t):
            S, I, R = vetor
            dS = -beta * S * I / N
            dI = beta * S * I / N - gamma * I
            dR = gamma * I
            return [dS, dI, dR]

        resultado = odeint(modelo_sir, [S0, I0, R0], t)

        return resultado
