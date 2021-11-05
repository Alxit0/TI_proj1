from main import np


def informacao_mutua(query, target, passo=1):
    def entropia(a):
        _, cnt = np.unique(a, return_counts=True, axis=0)
        prob = cnt/len(a)
        return np.sum(-1*prob*np.log2(prob))

    def entropia_conj(a, b):
        # same as entropia([*zip(a, b)])
        return entropia(np.c_[a, b])

    def inf_mutua(a, b):
        # H(a) + H(b) - Hconjunta(a, b)
        return entropia(a) + entropia(b) - entropia_conj(a, b)

    lenght = len(query)
    query = np.asarray(query)
    for i in range(0, len(target)-lenght, passo):
        temp = np.asarray(target[i:i+lenght])
        print(inf_mutua(query, temp))


if __name__ == '__main__':
    amostra = [2, 6, 4, 10, 5, 9, 5, 8, 0, 8]

    objetivo = [6, 8, 9, 7, 2, 4, 9, 9, 4, 9, 1, 4, 8, 0, 1, 2, 2, 6, 3, 2, 0, 7, 4, 9, 5,
                4, 8, 5, 2, 7, 8, 0, 7, 4, 8, 5, 7, 4, 3, 2, 2, 7, 3, 5]

    informacao_mutua(amostra, objetivo)
