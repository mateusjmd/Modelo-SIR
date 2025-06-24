import numpy as np
from scipy.integrate import odeint


def modelo_sir(vetor, t):
    """
    Calcula as derivadas das variáveis do modelo epidemiológico SIR

    Parâmetros:
    vetor: lista ou array contendo os valores atuais de [S, I, R] no tempo t
    t: tempo atual (passado automaticamente por odeint e não usado diretamente nessa função)

    Retorna:
    Retorna as variações populacionais (dS/dt, dI/dt, dR/dt) para cada compartimento no tempo t
    """
    S, I, R = vetor
    dS = -beta * S * I / N
    dI = beta * S * I / N - gamma * I
    dR = gamma * I
    return [dS, dI, dR]


# Definição e obtenção dos parâmetros
N = int(input('População Total: '))
I0 = int(input('Infectados iniciais: '))
R0 = 0 # Recuperados iniciais
S0 = N - I0 - R0 # Susceptíveis iniciais
beta = float(input('Taxa de Transmissão (β): '))
gamma = float(input('Taxa de Recuperação (γ): '))
dias = int(input('Dias de simulação: '))

# Período da simulação (dias)
t = np.linspace(0, dias, dias)

# Integra numericamente o sistema de equações diferenciais ao longo do período definido (t)
resultado = odeint(modelo_sir, [S0, I0, R0], t)