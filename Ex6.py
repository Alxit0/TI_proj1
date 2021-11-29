from main import np, get_matrix, plt


def informacao_mutua(query, target, passo=1):
    def inf_mutua(a, b) -> float:
        # H(a) + H(b) - Hconjunta(a, b)
        return entropia(a) + entropia(b) - entropia_conj(a, b)

    def entropia_conj(a, b):
        arry_temp = [*zip(a, b)]
        return entropia(arry_temp)

    def entropia(a):
        _, cnt = np.unique(a, return_counts=True, axis=0)  # achar as contagens
        prob = cnt / len(a)
        return np.sum(-1 * prob * np.log2(prob))

    lenght = len(query)  # tamanho
    query = np.asarray(query)
    final = []
    for i in range(0, len(target)-lenght+1, passo):
        temp = np.asarray(target[i:i+lenght])
        final += round(inf_mutua(query, temp), 4),  # adicionar o valor a lista final
    return np.asarray(final)


def visualizacao_dados(data: np.ndarray, a):
    fig, x = plt.subplots()
    x.plot(data)
    x.plot(a)
    plt.show()


if __name__ == '__main__':
    """
    Nao sei se o que eu fiz esta certo. Sei que a alinhea a) da o mesmo resultado
      e fiz o resto a partir dai.
    
    Na alinhea b) apenas gerei a matriz das ifm's da mesma forma do que na a) e depois puz
      num grafico
    
    Na alinjea c) gerei a matriz das ifm's para cada um dos ficheiros pretendidos
      e achei o maximo de cada uma delas.
    Nao achei o instante em que elas aparecem, achei o valor ifm em si,
      caso o stor queira o instante na musica vao ter de pensar no passo
      que estamos a dar. Mas provavelmente nao vai ser porque para isso iamos
      precisar da frequencia e nos estamos a perde-la. Caso seja vao ter de escrever
      uma funcao nova para gerar a matriz mas so para som.
      
    IMPORTANTE - nao se esquecao de ver como usar o alfabeto.
    """

    def alinhea_a():
        # nao sei para que serve o alfabeto aqui.
        amostra = [2, 6, 4, 10, 5, 9, 5, 8, 0, 8]

        objetivo = [6, 8, 9, 7, 2, 4, 9, 9, 4, 9, 1, 4, 8, 0, 1, 2, 2, 6, 3, 2, 0, 7, 4, 9, 5,
                    4, 8, 5, 2, 7, 8, 0, 7, 4, 8, 5, 7, 4, 3, 2, 2, 7, 3, 5, 2, 7, 4, 9, 9, 6]

        ifm = informacao_mutua(amostra, np.asarray(objetivo))
        print(ifm)

    def alinhea_b():
        amostra, _ = get_matrix("data_ex6/saxriff.wav", alfabeto="0-256")

        objetivo_1, _ = get_matrix("data_ex6/target01 - repeat.wav", alfabeto="0-256")
        objetivo_2, _ = get_matrix("data_ex6/target02 - repeatNoise.wav", alfabeto="0-256")

        ifm_1 = informacao_mutua(amostra, objetivo_1, passo=len(amostra)//4)  # target 01
        ifm_2 = informacao_mutua(amostra, objetivo_2, passo=len(amostra)//4)  # target 02
        print("target01 - repeat.wav =>", ifm_1)
        print("target02 - repeatNoise.wav =>", ifm_2)
        visualizacao_dados(ifm_1, ifm_2)

    def alinhea_c():
        # gerar os nomes para os ficheiros
        names = []
        for i in range(1, 8):
            temp_name = f"data_ex6/Song0{i}.wav"
            names += temp_name,

        # iniciar a query
        amostra, _ = get_matrix("data_ex6/saxriff.wav", alfabeto="0-256")
        d = {}
        # iterar pelos ficheiros e mostrar o ifm maximo
        for i in names:
            objetivo, _ = get_matrix(i, alfabeto="0-256")

            evolucao_ifm = informacao_mutua(amostra, objetivo, passo=len(amostra)//4)
            d[i[9:19]] = np.max(evolucao_ifm)
            print(end='#')

        for i in (sorted(d.keys(), key=d.__getitem__, reverse=True)):
            print(f"{i}: {d[i]}")

    # alinhea_a()
    # alinhea_b()
    alinhea_c()
