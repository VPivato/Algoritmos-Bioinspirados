import random
import matplotlib.pyplot as plt


def gera_prato():
    alimentos = []
    for i in range(5): # Para cada alimento que pode estar no prato, nesse estudo de caso
        quant = random.random() * 200 # Adiciona de 0 a 200 gramas aleatóriamente
        alimentos.append(quant)
    return alimentos


def gera_populacao(quantidade):
    populacao = []
    for i in range(quantidade):
        populacao.append(gera_prato())
    return populacao


def divergencia(prato, mostrar=False):
    # Peito de frango, batata-doce, arroz integral, ovo, feijão
    carboidratos = prato[0]*0.05 + prato[1]*0.24 + prato[2]*0.26 + prato[3]*0.015 + prato[4]*0.29 # Quantidade de carboidratos em cada alimento do prato
    proteinas = prato[0] * 0.23 + prato[1] * 0.02 + prato[2] * 0.026 + prato[3] * 0.13 + prato[4] * 0.095 # Quantidade de proteínas em cada alimento do prato
    lipideos = prato[0] * 0.05 + prato[1] * 0.00 + prato[2] * 0.01 + prato[3] * 0.089 + prato[4] * 0.014 # Quantidade de lipídeos em cada alimento do prato
    total = carboidratos + proteinas + lipideos
    soma = sum(prato)

    porcentagem_carboidratos = carboidratos / total * 100 # Porcentagem de carboidratos em relação ao total de nutrientes do prato
    porcentagem_proteinas = proteinas / total * 100 # Porcentagem de proteínas em relação ao total de nutrientes do prato
    porcentagem_lipideos = lipideos / total * 100 # Porcentagem de lipídeos em relação ao total de nutrientes do prato

    diferenca_carboidratos = abs(porcentagem_carboidratos - 55) # Diferença da porcentagem de carboidratos em relação à quantidade desejada (nesse estudo de caso, 55%)
    diferenca_proteinas = abs(porcentagem_proteinas - 30) # Diferença da porcentagem de proteínas em relação à quantidade desejada (nesse estudo de caso, 30%)
    diferenca_lipideos = abs(porcentagem_lipideos - 15) # Diferença da porcentagem de lipídeos em relação à quantidade desejada (nesse estudo de caso, 15%)

    diferenca_total = round(diferenca_carboidratos + diferenca_proteinas + diferenca_lipideos, 4) # Diferença em relação ao prato desejado, quanto mais perto de zero, melhor

    if mostrar:
        print(f"Carboidratos: {porcentagem_carboidratos:.3f}% / 55%")
        print(f"Proteínas: {porcentagem_proteinas:.3f}% / 30%")
        print(f"Lipídeos: {porcentagem_lipideos:.3f}% / 15%")
        print(f"Peso total: {soma:.2f}g")

    return diferenca_total


def seleciona_tres(pai, populacao):
    populacao_2 = []
    tres_escolhidos = []
    for i in populacao: # Itera a população
        if i != pai:
            populacao_2.append(i) # Adiciona à populacao_2 todos os items diferentes do vetor pai

    for i in range(3): # Seleciona três vetores diferentes entre si e diferentes do vetor pai
        aleatorio = random.choice(populacao_2)
        tres_escolhidos.append(aleatorio)
        populacao_2.remove(aleatorio)

    return tres_escolhidos


def mutacao(vetor_pai, tres_vetores , _cr, _f):
    # CR > probabilidade de aplicar o operador de mutação (0-1)
    # F > peso diferencial, o quão diferente a tentativa será do vetor pai (0-2)

    a = tres_vetores[0]
    b = tres_vetores[1]
    c = tres_vetores[2]

    tentativa = []
    for i in range(len(vetor_pai)):
        rand = random.random() # Gera um número aleatório de 0 a 1
        if rand < _cr:
            x = a[i] + _f * (b[i] - c[i]) # Fórmula usada no algoritmo de evolução diferencial para gerar um gene diferente
        else:
            x = vetor_pai[i]
        tentativa.append(x)
    return tentativa


def melhor_vetor(pop):
    notas = [divergencia(i) for i in pop] # Adiciona o valor de divergência para cada cromossomo da população
    indice = notas.index(min(notas)) # Pega o índice do menor valor de notas
    return indice


def evolucao_diferencial(numero_populacao, quantidade_iteracoes, chance_crossover=0.3, peso_diferencial=0.8, plot=False):
    melhores = []
    populacao = gera_populacao(numero_populacao) # Gera uma população

    """Itera X vezes para cada vetor na população. Por exemplo, se quantidade_iteracoes for 100, e numero_populacao for 10,
       para cada um dos 10 indivíduos, gera 100 vetores tentativa com base no operador de mutação. No fim, armazena apenas
       a melhor tentativa dessas 100 iterações."""
    for i in range(quantidade_iteracoes): # Loop baseado na quantidade de iterações/gerações definidas
        for vetor in populacao: # Itera em todos os cromossomos da população
            tres_vetores = seleciona_tres(vetor, populacao) # Seleciona tres indivíduos diferentes
            tentativa = mutacao(vetor, tres_vetores, chance_crossover, peso_diferencial) # Faz uma tentativa de mutação com base no vetor pai (o que está sendo iterado atualmente)
                                                                                         # E os três outros vetores escolhidos
            if divergencia(tentativa) < divergencia(vetor): # Se o fitness da tentativa for melhor que o do vetor pai
                populacao.remove(vetor) # Remove o pai da população
                populacao.append(tentativa) # Adiciona a tentativa na população
        melhores.append(divergencia(populacao[melhor_vetor(populacao)])) # Pega o melhor indivíduo de cada geração/iteração
    if plot:
        plt.plot(melhores)
        plt.title("Evolução das Divergências")
        plt.xlabel("Iterações")
        plt.ylabel("Divergência")
        plt.show()

    # No fim, a população terá a mesma quantidade de indivíduos que no começo
    return populacao[melhor_vetor(populacao)] # Retorna o melhor individuo da população


if __name__ == "__main__":
    # Peito de frango, batata-doce, arroz integral, ovo, feijão
    F = 0.8 # Paramêtro que define o quão diferente o vetor tentativa será do vetor pai, geralmente é um valor entre 0 e 2
    CR = 0.3 # Define a probabilidade de aplicar o operador de diferenciação (mistura entre crossover/mutação)

    resultado = evolucao_diferencial(250, 150, CR, F, plot=True)
    print(resultado)
    print(f"Valor de Fitness: {divergencia(resultado, mostrar=True)}")

