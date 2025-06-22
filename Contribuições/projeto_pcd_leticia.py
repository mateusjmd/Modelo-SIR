def obter_dados_varias_cidades():
    num_cidades = int(input("Quantas cidades participarão da simulação? "))
    cidades = []
    parametros = {}

    for i in range(num_cidades):
        nome = input(f"\nNome da cidade {i + 1}: ")
        cidades.append(nome)

        print(f"Parâmetros para {nome}:")
        S = int(input("  Número de suscetíveis: "))
        I = int(input("  Número de infectados: "))
        R = int(input("  Número de recuperados: "))

        total = S + I + R
        if total == 0:
            print("  Erro: a população total não pode ser zero.")
            return None

        parametros[nome] = {"S": S, "I": I, "R": R}

    beta = float(input("\nInsira o valor de beta (taxa de transmissão, entre 0 e 1): "))
    if not (0 <= beta <= 1):
        print("Erro: beta deve estar entre 0 e 1.")
        return None

    gamma = float(input("Insira o valor de gamma (taxa de recuperação, entre 0 e 1): "))
    if not (0 <= gamma <= 1):
        print("Erro: gamma deve estar entre 0 e 1.")
        return None

    print("\nAgora informe quantas pessoas infectadas viajam diariamente de uma cidade para outra:")
    mobilidade = {}
    for origem in cidades:
        for destino in cidades:
            if origem != destino:
                chave = (origem, destino)
                viajantes = int(input(f"  {origem} → {destino}: "))
                mobilidade[chave] = viajantes

    return cidades, parametros, mobilidade, beta, gamma