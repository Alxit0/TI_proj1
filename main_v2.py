import numpy as np
import matplotlib.image as mpimg
from scipy.io import wavfile
from matplotlib import pyplot as plt
from math import log2
import huffmancodec as huf


class dados:
    def __init__(self, nome_ficheiro):
        self._type = 'num'  # iniciar o tipo de dados para depois saber como defifrar
        # camiho para o ficheiro
        # IMPORTANTE - ter os ficheiros numa pasta chamada de 'data'
        fonte = 'data/' + nome_ficheiro
        tipo = nome_ficheiro.split('.')[-1]
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
            temp = np.asarray([i for i in r if i.isalpha() or i == ' '])
            self._type = 'alpha'  # mudar o tipo de dados
        elif tipo == 'wav':
            # som
            f, temp = wavfile.read(fonte)

        temp = np.asarray([*map(str, temp)])
        '''
        # creation
        if shape == 2:
            # caso seja para agrupar de 2 em 2
            # retirar elemento extra caso o num de elementos seja impar
            desvio = temp.shape[0] % shape
            if desvio != 0:
                temp = temp[:-desvio]

            temp = np.asarray(  # transformar tudo en ndarray
                [*map(
                    lambda x: ' '.join(map(str, x)),  # transformar em str com espacos
                    np.reshape(temp, (temp.shape[0] // 2, 2)))  # mudar a forma para 2 em 2
                 ]
            )
        '''

        d = self._get_contagem(temp)

        # gurdar dados
        self.dados = temp
        self.contagem = d
        self.passo = 1

        # utilizador nao precisa de acesso visto que serve para apenas nao perder dados
        self._extras = []

    @staticmethod
    def _get_contagem(dado) -> dict:
        d = {}
        # obter contagem
        for i in dado:
            if i in d:
                d[i] += 1
            else:
                d[i] = 1
        return d

    def get_alfabeto(self):
        return self.contagem.keys()

    def histograma(self) -> None:
        plt.figure()
        plt.bar(self.contagem.keys(), self.contagem.values())
        plt.show()

    def get_entropia(self):
        temp = self.dados.shape[0]  # obter tamanho (len, ??)[0]
        prob = [i / temp for i in self.contagem.values()]  # obter as probabilades de cada elemento
        return -sum(i * log2(i)for i in prob) / self.passo

    def reshape(self, pace: int) -> None:
        # se o pace for igual ao passo atual na faz sentido continuar
        if pace == self.passo:
            return

        # escolher como e que vou descoficar as strings
        # se os elemsntos eram originalmente str: os caracteres que queremos sao os que estao posiscoes pares
        # se os elementos eram originalmente num: posso dar os str.split() (Nao era possival para
        #    o primeiro casp pois caso os chr fosse ' ', nao o ia apanhar)
        y = [lambda x:[*x[::2]], lambda x:x.split()][self._type == 'num']  # separar
        self.dados = np.append(
            np.asarray([*map(y, self.dados)]),  # passar os dados atuais pelo metode de descoficacao
            self._extras
        )  # ao dar np.append() a matriz ja vem em numa array de 1D.
        self._extras = []  # restirar os extras visto que ja os adicionamos

        # print(self.dados)
        tam = self.dados.shape[0]
        desvio = tam % pace  # quantos caracters estao a mais para uma diviaso sem restos
        if desvio > 0:
            self._extras = self.dados[-desvio:]  # gurdar os elementos que vamos tirar
            self.dados = self.dados[:-desvio]  # tirar os elemntos
            # IMPORTANTE - tem ser por esta ordem

        # caso o pace fosse 1, eu ja tinha a matriz visto que pace=1 == matriz.flaten()
        if pace != 1:
            self.dados = np.asarray(
                [*map(
                    lambda x:' '.join(map(str, x)),  # juntar os elemntos em forma de str
                    np.reshape(self.dados, (tam//pace, pace))  # por a matriz no pace que desejamos
                )]
            )

        # obter a nova conagem dos 'novos' dados.
        d = self._get_contagem(self.dados)

        self.contagem = d  # salvar a contagem dos novos dados
        self.passo = pace  # salvar o novo pace


def entropia_huf(f: dados):
    tam = f.dados.shape[0]
    codec = huf.HuffmanCodec.from_data(f.dados)
    # t = codec.get_code_table()  # key : (numbero de bits, valor representado pelos bits)

    s, l = codec.get_code_len()

    d = [f.contagem[i] * j / tam for i, j in zip(s, l)]
    return sum(d)


values = ['english.txt', 'guitarSolo.wav', 'homer.bmp', 'homerBin.bmp', 'kid.bmp']
if __name__ == '__main__':

    fich = dados(values[0])  # inicializar

    print(fich.dados)
    fich.reshape(3)
    print(fich.dados, fich.dados.shape)
    fich.reshape(2)
    print(fich.dados)
    fich.reshape(1)
    print(fich.dados, fich.dados.shape)
