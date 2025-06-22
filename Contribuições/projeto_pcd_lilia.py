def simulador_sir(cidades, parametros, mobilidade, beta, gamma, dias):
    resultados = {}
 
    for cidade in cidades:
        S = parametros[cidade]["S"]
        I = parametros[cidade]["I"]
        R = parametros[cidade]["R"]
        N = S + I + R
 
        historico = {
            "S": [S],
            "I": [I],
            "R": [R]
        }
 
        resultados[cidade] = {
            "S": [S],
            "I": [I],
            "R": [R],
            "N": N
        }
 
    for t in range(dias):
        novos_parametros = {}
 
        for cidade in cidades:
            S = resultados[cidade]["S"][-1]
            I = resultados[cidade]["I"][-1]
            R = resultados[cidade]["R"][-1]
            N = resultados[cidade]["N"]
 
          
            importados = 0
            for origem in cidades:
                if origem != cidade:
                    viajantes = mobilidade.get((origem, cidade), 0)
                    I_origem = resultados[origem]["I"][-1]
                    N_origem = resultados[origem]["N"]
                    if N_origem > 0:
                        prop_inf = I_origem / N_origem
                        importados += viajantes * prop_inf
 
            novos_infectados = beta * S * I / N
            novos_recuperados = gamma * I
 
            S_novo = S - novos_infectados
            I_novo = I + novos_infectados - novos_recuperados + importados
            R_novo = R + novos_recuperados
 
            novos_parametros[cidade] = (S_novo, I_novo, R_novo)
 
        # Atualiza os dados após o dia
        for cidade in cidades:
            S_novo, I_novo, R_novo = novos_parametros[cidade]
            resultados[cidade]["S"].append(S_novo)
            resultados[cidade]["I"].append(I_novo)
            resultados[cidade]["R"].append(R_novo)
 
    return resultados