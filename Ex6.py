from main import np, get_matrix, values, plt


def informacao_mutua(query, target, passo=1):
    def entropia(a):
        _, cnt = np.unique(a, return_counts=True, axis=0)
        prob = cnt/len(a)
        return np.sum(-1*prob*np.log2(prob))

    def entropia_conj(a, b):
        # o mesmo que entropia([*zip(a, b)])
        return entropia(np.c_[a, b])

    def inf_mutua(a, b) -> float:
        # H(a) + H(b) - Hconjunta(a, b)
        return entropia(a) + entropia(b) - entropia_conj(a, b)

    lenght = len(query)
    query = np.asarray(query)
    final = []
    for i in range(0, len(target)-lenght+1, passo):
        temp = np.asarray(target[i:i+lenght])

        final += round(inf_mutua(query, temp), 4),
    return np.asarray(final)


def visualizacao_dados(data: np.ndarray):
    plt.figure()
    plt.plot([*range(len(data))], data)
    plt.show()
    # plt.close()


if __name__ == '__main__':
    def alinhea_a():
        # nao sei para que serve o alfabeto aqui.
        amostra = [2, 6, 4, 10, 5, 9, 5, 8, 0, 8]

        objetivo = [6, 8, 9, 7, 2, 4, 9, 9, 4, 9, 1, 4, 8, 0, 1, 2, 2, 6, 3, 2, 0, 7, 4, 9, 5,
                    4, 8, 5, 2, 7, 8, 0, 7, 4, 8, 5, 7, 4, 3, 2, 2, 7, 3, 5, 2, 7, 4, 9, 9, 6]

        ifm = informacao_mutua(amostra, np.asarray(objetivo))
        print(ifm)

    def alinhea_b():
        # inacaba porque ainda nao da para ver a variacao mas ja temos os resultados
        amostra, _ = get_matrix("data_ex6/saxriff.wav", alfabeto="0-256")

        objetivo_1, _ = get_matrix("data_ex6/target01 - repeat.wav", alfabeto="0-256")
        objetivo_2, _ = get_matrix("data_ex6/target02 - repeatNoise.wav", alfabeto="0-256")

        print("query  ->", amostra)
        print("target ->", objetivo_1)

        ifm = informacao_mutua(amostra, objetivo_1, passo=len(amostra)//4)  # target 01
        # ifm = informacao_mutua(amostra, objetivo_2, passo=len(amostra)//4)  # target 02

        print(ifm)
        visualizacao_dados(ifm)

    def alinhea_c():
        # gerar os nomes para os ficheiros
        names = []
        for i in range(1, 8):
            temp_name = f"data_ex6/Song0{i}.wav"
            names += temp_name,

        # iniciar a query
        amostra, _ = get_matrix("data_ex6/saxriff.wav", alfabeto="0-256")

        # iterar pelos ficheiros e mostrar o ifm maximo
        for i in names:
            objetivo, _ = get_matrix(i, alfabeto="0-256")

            evolucao_ifm = informacao_mutua(amostra, objetivo, passo=len(amostra)//4)
            print(i[9:15]+" -> ", np.max(evolucao_ifm))  # informacao mutua maxima

    '''
    IMPORTANTE - ter os ficheiros para este exercicio numa pasta chamada 'data_ex6'
    IMPORTANTE - Na alinhea b) nao sei como fechar um grafico depois de algum tempo e depois abrir outro
                   se quiserem ver os dois tem de os mudar (basta 'descomentar' um e comentar o outro)
                 Se quizerem trabalhar nisso nao reclamo.
    IMPORTANTE - Na alinhea c) do 'Song05' ate ao final demora uns segundos mas nao se preocupem
                   que ele corre. Nao sei onde melhorar mais
    '''

    # alinhea_a()
    # alinhea_b()
    alinhea_c()
