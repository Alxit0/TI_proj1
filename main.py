from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from math import log2
import numpy as np
from scipy.io import wavfile
import huffmancodec as huf


def get_matrix(nome_ficheiro, shape=1, alfabeto=''):
    """
    :param nome_ficheiro: Nome do ficheiro
    :param shape: passo para organizar a informacao (default = 1)
    :param alfabeto: setar o alfabeto (so funciona caso o 'shape' = 1)
    a-z => todas as letras de 'a' a 'z'
    A-Z => versao 'a-z' mas em maiusculas
    x-y => (em que x,y pertencem a N) numeros do x ate ao y
    :return: ndarray de dados, contagem em forma de dicionario
    """
    # camiho para o ficheiro
    # IMPORTANTE - ter os ficheiros numa pasta chamada de 'data'
    if nome_ficheiro.count("/")==0:
        fonte = 'data/' + nome_ficheiro
    else:
        fonte = nome_ficheiro
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
        if len(temp.shape) != 1:
            temp = temp[:, 0]  # so apanhar o primeiro canal (nao sei se o 0 é o esquerdo ou o direito)

    # creation
    if shape == 2:
        # retirar elemento extra caso o num de elementos seja impar
        desvio = temp.shape[0] % shape
        if desvio != 0:
            temp = temp[:-desvio]

        temp = np.asarray(  # transformar tudo en ndarray
            [*map(
                lambda x: ' '.join(map(str, x)),  # transformar em str com espacos
                np.reshape(temp, (temp.shape[0] // 2, 2))  # mudar a forma para 2 em 2
                    )
             ]
        )
        # obter a contagem sem elementos a zero (sem usar o alfabeto)
        d = {}
        for i in temp:
            if i in d:
                d[i] += 1
            else:
                d[i] = 1
    else:
        # so de um em um
        parcelas = alfabeto.split(',')
        d = {}
        for j in parcelas:
            if j.split('-')[0].isalpha():
                # caso sejam letras
                inicio, fim = sorted(j.split('-'))
                for i in range(ord(inicio), ord(fim)+1):
                    d[chr(i)] = 0
            else:
                # caso sejam numeros
                inicio, fim = sorted(map(int, j.split('-')))
                for i in range(int(inicio), int(fim)+1):
                    d[i] = 0
        # print(d)

        # obter contagem utilizando o alfabeto (tem zeros)
        for i in temp:
            if i in d:
                d[i] += 1

    return temp, d  # dados do ficherio organizados, contagem(alfabeto = d.keys())


def histograma(cont: dict):
    #  mostra o histograma num grafico de barras
    plt.figure()
    plt.bar(cont.keys(), cont.values())
    plt.show()
    plt.close()


def entropia(data: np.ndarray, cont):
    tam = data.shape[0]
    prob = np.asarray(list(cont.values()))  # passar os valores para ndarray
    prob = prob[prob.nonzero()]/tam  # tirar os zeros e dividir pelo tamanho

    return sum(-log2(x)*x for x in prob)


def entropia_huf(data, cont):
    tam = data.shape[0]
    codec = huf.HuffmanCodec.from_data(data)
    # t = codec.get_code_table()  # key : (numbero de bits, valor representado pelos bits)

    s, l = codec.get_code_len()

    d = [cont[i] * j / tam for i, j in zip(s, l)]
    return sum(d)


values = ['english.txt', 'guitarSolo.wav', 'homer.bmp', 'homerBin.bmp', 'kid.bmp']
if __name__ == '__main__':
    passo = 1
    dados, contagem = get_matrix(values[1], passo, '0-260')
    # print(dados)
    # print(contagem)
    print(entropia(dados, contagem) / passo)
    print(entropia_huf(dados, contagem) / passo)
