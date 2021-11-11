import numpy as np

from main import get_matrix, huf
from main import values as v


def media(probs, lenghts):
    media = 0
    for i in range(len(lenghts)):
        media += lenghts[i]*probs[i]
        print(media)
    return media

def variancia(probs, media, lenghts):
    var = 0
    for i in range(len(lenghts)):
        var += (probs[i]*(lenghts[i]-media)**2)
    return var


values, conts = get_matrix(v[2],1, "a-z,A-Z")
tam = values.shape[0]
codec = huf.HuffmanCodec.from_data(values)
t = codec.get_code_table()  # key : (numbero de bits, valor representado pelos bits)

probs = []
lenghts = []
l=len(values)
for i,j in t.values():
    lenghts+=i,
    probs+=j/l,

print(lenghts)
print(np.var(lenghts))