import time, random

pessoas = [("Lisbon", "LIS"),
           ("Madrid", "MAD"),
           ("Paris", "CDG"),
           ("Dublin", "DUB"),
           ("Brussels", "BRU"),
           ("London", "LHR")]
destino = "FCO" # Roma
voos = {}
for linha in open("flights.txt", "r"):
    _origem, _destino, _saida, _chegada, _preco = linha.split(",")
    voos.setdefault((_origem, _destino), [])
    voos[_origem, _destino].append((_saida, _chegada, int(_preco)))


def imprime_calendario(calendario):
    voo_id = -1
    preco_total = 0
    for i in range(len(calendario) // 2): # Divide por dois porque são dois voos para cada pessoa
        nome_cidade = pessoas[i][0] # Pega o nome da cidade
        origem = pessoas[i][1] # Pega a sigla do aeroporto

        voo_id += 1
        voo_ida = voos[(origem, destino)][calendario[voo_id]] # Pega o voo de ida baseado no parametro calendário recebido
        preco_total += voo_ida[2] # Adiciona o preço do voo de ida

        voo_id += 1
        voo_volta = voos[(destino, origem)][calendario[voo_id]] # Pega o voo de volta baseado no parametro calendário recebido
        preco_total += voo_volta[2] # Adiciona o preço do voo de volta

        print(f"{nome_cidade:<10} {origem:<5} {voo_ida[0]:>5}-{voo_ida[1]:<5} U${voo_ida[2]:<5} {voo_volta[0]:>5}-{voo_volta[1]:<5} U${voo_volta[2]:<5}")
    print(f"Preço total das passagens: U${preco_total}")


def get_minutos(hora):
    t = time.strptime(hora, "%H:%M") # Formata string de tempo em um objeto struct_time
    minutos = t[3] * 60 + t[4] # Horas * 60 + minutos
    return minutos


def get_espera(calendario):
    espera_total = 0
    ultima_chegada = 0
    primeira_partida = 1439  # 23:59
    voo_id = -1

    for i in range(len(calendario) // 2):  # Divide por dois porque são dois voos para cada pessoa
        origem = pessoas[i][1]

        voo_id += 1
        voo_ida = voos[(origem, destino)][calendario[voo_id]]  # Pega o voo de ida baseado no parametro calendário recebido

        voo_id += 1
        voo_volta = voos[(destino, origem)][calendario[voo_id]]  # Pega o voo de volta baseado no parametro calendário recebido

        # Atualiza as variáveis e pega o valor da última chegada e primeira partida do calendário
        if ultima_chegada < get_minutos(voo_ida[1]):
            ultima_chegada = get_minutos(voo_ida[1])
        if primeira_partida > get_minutos(voo_volta[0]):
            primeira_partida = get_minutos(voo_volta[0])

    voo_id = -1
    for i in range(len(calendario) // 2):  # é preciso fazer outro loop, pois apenas após o término do primeiro que as variáveis
                                           # ultima_chegada e primeira_partida estarão preenchidas
        origem = pessoas[i][1]

        voo_id += 1
        voo_ida = voos[(origem, destino)][
            calendario[voo_id]]  # Pega o voo de ida baseado no parametro calendário recebido

        voo_id += 1
        voo_volta = voos[(destino, origem)][
            calendario[voo_id]]  # Pega o voo de volta baseado no parametro calendário recebido

        espera_total += ultima_chegada - get_minutos(voo_ida[1])
        espera_total += get_minutos(voo_volta[0]) - primeira_partida
    return espera_total

def funcao_avaliacao(calendario):
    preco_total = 0
    espera_total = 0
    ultima_chegada = 0
    primeira_partida = 1439 # 23:59
    voo_id = -1

    for i in range(len(calendario) // 2):  # Divide por dois porque são dois voos para cada pessoa
        origem =  pessoas[i][1]

        voo_id += 1
        voo_ida = voos[(origem, destino)][calendario[voo_id]]  # Pega o voo de ida baseado no parametro calendário recebido
        preco_total += voo_ida[2]  # Adiciona o preço do voo de ida

        voo_id += 1
        voo_volta = voos[(destino, origem)][calendario[voo_id]]  # Pega o voo de volta baseado no parametro calendário recebido
        preco_total += voo_volta[2]  # Adiciona o preço do voo de volta

        # Atualiza as variáveis e pega o valor da última chegada e primeira partida do calendário
        if ultima_chegada < get_minutos(voo_ida[1]):
            ultima_chegada = get_minutos(voo_ida[1])
        if primeira_partida > get_minutos(voo_volta[0]):
            primeira_partida = get_minutos(voo_volta[0])

    voo_id = -1
    for i in range(len(calendario) // 2):  # é preciso fazer outro loop, pois apenas após o término do primeiro que as variáveis
                                           # ultima_chegada e primeira_partida estarão preenchidas
        origem =  pessoas[i][1]

        voo_id += 1
        voo_ida = voos[(origem, destino)][calendario[voo_id]]  # Pega o voo de ida baseado no parametro calendário recebido

        voo_id += 1
        voo_volta = voos[(destino, origem)][calendario[voo_id]]  # Pega o voo de volta baseado no parametro calendário recebido

        espera_total += ultima_chegada - get_minutos(voo_ida[1])
        espera_total += get_minutos(voo_volta[0]) - primeira_partida
    return espera_total + preco_total


def mutacao(_dominio, _calendario, _probabilidade=0.05, _passo=1):
    gene = random.randint(0, len(_dominio) -1)
    mutante = _calendario[:]
    if random.random() < _probabilidade:
        if _calendario[gene] != _dominio[gene][0]: # Compara com o valor mínimo do domínio
            mutante[gene] -= _passo
        else:
            if _calendario[gene] != _dominio[gene][1]: # Compara com o valor máximo do domínio
                mutante[gene] += _passo
    return mutante


def crossover(_dominio, individuo1, individuo2):
    gene = random.randint(1, len(dominio) - 2) # Ponto de corte, não é possível fazer o crossover no índice zero ou máximo
    return individuo1[:gene] + individuo2[gene:] # Concatena os pais e retorna um cromossomo cruzado


def algoritmo_genetico(_dominio, _funcao_avaliacao, _tamanho_populacao=200, _numero_geracoes=200, _elitismo=0.2, _probabilidade_mutacao=0.1, _passo=1):
    populacao = []
    custos = []
    for i in range(_tamanho_populacao): # Criação da população inicial de forma randômica
        individuo = [random.randint(_dominio[i][0], _dominio[i][1]) for i in range(len(dominio))] # Gera uma lista com 12 números de 0 a 9 (mínimo e máximo do domínio)
        populacao.append(individuo)

    numero_elitismo = int(_elitismo * _tamanho_populacao) # Quantos dos melhores cromossomos serão selecionados

    # Loop principal do algoritmo genético
    for i in range(_numero_geracoes):
        custos = [(_funcao_avaliacao(individuo), individuo) for individuo in populacao] # Adiciona um índice [(custo, individuo)] para cada cromossomo da população
        custos.sort() # Ordena do menor para o maior
        individuos_ordenados = [individuo for (_, individuo) in custos] # Cria uma lista apenas com os indivíduos, do melhor (custo mais baixo) até o pior (custo mais alto)

        populacao = individuos_ordenados[:numero_elitismo] # Reescreve a população com os melhores X indivíduos da população (baseado no elitismo)

        while len(populacao) < _tamanho_populacao: # Repopula a população baseado nos melhores indivíduos selecionados
            individuo1 = 0
            individuo2 = 0
            while individuo1 == individuo2: # Evita que o mesmo indivíduo seja selecionado para o crossover
                individuo1 = random.randint(0, numero_elitismo)
                individuo2 = random.randint(0, numero_elitismo)
            novo_individuo = crossover(_dominio, individuos_ordenados[individuo1], individuos_ordenados[individuo2])
            mutacao_novo_individuo = mutacao(_dominio, novo_individuo, _probabilidade=_probabilidade_mutacao)
            populacao.append(mutacao_novo_individuo)
    return custos[0][1] # Retorna o cromossomo da melhor solução


if __name__ == "__main__":
    dominio = [(0, 9)] * len(pessoas) * 2
    solucao = algoritmo_genetico(dominio, funcao_avaliacao)
    espera = get_espera(solucao)
    custo_solucao = funcao_avaliacao(solucao)

    print(f"Cromossomo: {solucao}")
    imprime_calendario(solucao)
    print(f"Tempo total de espera: {espera} min")
    print(f"Métrica de avaliação: {custo_solucao} pts.") # Métrica de avaliação = custo_passagens + espera_total