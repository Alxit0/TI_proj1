# Ver como é que o alfabeto que estamos a por como parametro funciona:
# É parecido com o sistema que é usado na biblioteca do regex.
# VEJAM TUDO ATE AO FINAL

def generate_alfabeto(al: str):
    parcelas = al.split(',')
    d = []
    for j in parcelas:
        if j.split('-')[0].isalpha():
            # caso sejam letras
            inicio, fim = sorted(j.split('-'))
            for i in range(ord(inicio), ord(fim) + 1):
                d += chr(i),
        else:
            # caso sejam numeros
            inicio, fim = sorted(map(int, j.split('-')))
            for i in range(int(inicio), int(fim) + 1):
                d += i,
    return list(d)


# tipo 1 - numeros
string = "0-100"  # numeros de um 0 a 100 (inclusive)
print(generate_alfabeto(string))
string = "5-324"  # numeros de um 5 a 324 (inclusive)
print(generate_alfabeto(string))

# tipo 2 - letras minusculas
string = "a-z"  # letras do 'a' ao 'z' (inclusive)
print(generate_alfabeto(string))
string = "d-h"  # letras do 'a' ao 'z' (inclusive)
print(generate_alfabeto(string))

# tipo 3 - letras maiusculas
string = "A-Z"  # letras do 'A' ao 'Z' (inclusive)
print(generate_alfabeto(string))
string = "F-K"  # letras do 'F' ao 'F' (inclusive)
print(generate_alfabeto(string))

"""
IMPORTANTE:
Nao misturem tipos.  ex: "a-Z" ou "S-23"
Nao metam negativos. ex: "-2-10"

PROPRIEDADES:

mutabilidade: "a-h" = "h-a"
multidade:    "a-h,1-4" -> ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 1, 2, 3, 4]
        logo: "a-h,w-z" -> ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'w', 'x', 'y', 'z']
"""
