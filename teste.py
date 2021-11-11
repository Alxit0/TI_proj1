from main import np, mpimg, wavfile


def get_matrix(nome_ficheiro, shape=1, alfabeto=''):
    """
    :param nome_ficheiro: Nome do ficheiro
    :param shape: passo para organizar a informacao (default = 1)
    :param alfabeto: setar o alfabeto (so funciona caso o 'shape' = 1)
    a-z => todas as letras de 'a' a 'z'
    A-Z => versao 'a-z' mass em maiusculas
    x-y => (em que x,y pertencem a N) numeros do x ate ao y
    :return: ndarray de dados, contagem em forma de dicionario
    """
    # caminho para o ficheiro
    # IMPORTANTE - ter os ficheiros numa pasta chamada de 'data'
    if nome_ficheiro.count("/") == 0:
        fonte = 'data/' + nome_ficheiro
    else:
        fonte = nome_ficheiro
    tipo = fonte.split('.')[-1]  # obter o tipo de ficheiro
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

    # criaçao
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
