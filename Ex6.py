from main import np
query = [2, 6, 4, 10, 5, 9, 5, 8, 0, 8]

target = [6, 8, 9, 7, 2, 4, 9, 9, 4, 9, 1, 4, 8, 0, 1, 2, 2, 6, 3, 2, 0, 7, 4, 9, 5,
          4, 8, 5, 2, 7, 8, 0, 7, 4, 8, 5, 7, 4, 3, 2, 2, 7, 3, 5]


def entropia(X):
    unique, cnt = np.unique(X, return_counts=True, axis=0)
    prob = cnt/len(X)
    en = np.sum((-1)*prob*np.log2(prob))
    return en


def EntropiaConj(X, Y):
    XY = np.c_[X, Y]
    return entropia(XY)


def EntropiaCond(X, Y):
    return EntropiaConj(X, Y) - entropia(Y)


def inf_mutua(X, Y):
    return entropia(X) + entropia(Y) - EntropiaConj(X, Y)


lenght = len(query)
passo = 1
query = np.asarray(query)
for i in range(0, len(target)-lenght, passo):
    temp = np.asarray(target[i:i+lenght])
    a = inf_mutua(query, temp)
    print(a)
