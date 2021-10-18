from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from math import log2
import numpy as np
from scipy.io import wavfile
import huffmancodec as huf


def get_matrix(nome_ficheiro, shape=1):
    # camiho para o ficheiro
    # IMPORTANTE - ter os ficheiros numa pasta chamada de 'data'
    fonte = 'data/' + nome_ficheiro
    tipo = fonte.split('.')[-1]  # obter o tipo de fixeiro
    temp = None

    # obter informaçao do ficheiro dependedo do tipo
    if tipo == 'bmp':
        # imagem
        img = np.asarray(mpimg.imread(fonte))
        temp = img.flatten()
    elif tipo == 'txt':
        # texto
        with open(fonte, 'r') as file:
            r = ''.join(file.readlines()).replace('\n', '')
        temp = np.asarray([i for i in r if i.isalpha()])
    elif tipo == 'wav':
        # som
        f, temp = wavfile.read(fonte)

    # creation
    alf_base = set(temp)  # alfabeto base
    if shape == 2:
        # caso seja para agrupar de 2 em 2
        d = {f'{i} {j}': 0 for i in alf_base for j in alf_base}
        # retirar elemento extra caso o num de elementos seja impar
        desvio = temp.shape[0] % shape
        if desvio != 0:
            temp = temp[:-desvio]

        if shape > 1:
            temp = np.asarray(  # transformar tudo en ndarray
                [*map(
                    lambda x: ' '.join(map(str, x)),  # transformar em str com espacos
                    np.reshape(temp, (temp.shape[0] // 2, 2))  # mudar a forma para 2 em 2
                        )
                 ]
            )
    else:
        # so de um em um
        d = {i: 0 for i in alf_base}

    # obter a contagem
    for i in temp:
        if i in d:
            d[i] += 1

    return temp, d  # dados do ficherio organizados, contagem(alfabeto = d.keys())


def histogram(cont: dict):
    #  mostra o histograma num grafico de barras
    plt.figure()
    plt.bar(cont.keys(), cont.values())
    plt.show()
    plt.close()


def entropia(data: np.ndarray, cont):
    temp = data.shape[0]
    prob = [i / temp for i in cont.values()]
    return -sum(i * log2(i) for i in prob if i != 0)


def entropia_huf(data, cont):
    tam = data.shape[0]
    codec = huf.HuffmanCodec.from_data(data)
    # t = codec.get_code_table()  # key : (numbero de bits, valor representado pelos bits)

    s, l = codec.get_code_len()

    d = [cont[i] * j / tam for i, j in zip(s, l)]
    return sum(d)


values = ['english.txt', 'guitarSolo.wav', 'homer.bmp', 'homerBin.bmp', 'kid.bmp']
if __name__ == '__main__':
    passo = 2
    dados, contagem = get_matrix(values[4], passo)

    print(entropia_huf(dados, contagem) / passo)
