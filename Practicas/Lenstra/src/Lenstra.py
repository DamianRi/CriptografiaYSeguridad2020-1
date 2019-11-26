#! /usr/bin/python3

"""
### Autores:
- Tadeo Guillén Diana G
- Rivera González Damián
- - -
Nota: Código implementado con Python 3.6.9

Dependencias:

Se debe tener instalado el paquete **PyCryptodome**, si se tiene configurado Python 3 de manera adecuada en la computadora y teniendo instalado Pip 3, es suficiente con ejecutar el siguiente comando para descargar el paquete:
```
    $ pip3 install pycryptodome
```
De otra manera se deja el enlace para su instalación [**PyCryptodome**](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)

- - -
"""


from Crypto.Util import number
import sys

#num = 1073561597    // Número a factorizar
#NUM = 87463
NUM = 35

class Punto:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lam = 0
        self.num = 0
        self.den = 0

def modn(x):
    return (x+NUM)%NUM

def suma_puntos_diferentes(p, q):
    pr = Punto(0,0)

    if p.x == 0 and p.y == 0:
        return q
    if q.x == 0 and q.y == 0:
        return p
    if (p.x == q.x) and (q.x == (-1*p.y)):
        return pr

    pr.lam = modn((q.y-p.y)*number.inverse(q.x - p.x, NUM))
    pr.num = modn(q.y - p.y)
    pr.den = modn(q.x + p.x)
    pr.x = modn (modn (pr.lam * pr.lam) + modn ((-1 * p.x)) + modn ((-1 * q.x)))
    pr.y = modn ((pr.lam * (p.x - pr.x)) - p.y)
    return pr

def suma_puntos_iguales(p):
    pr = Punto(0,0)
    pr.lam = modn (((3 * (p.x * p.x)) + a) * number.inverse(p.y * 2, NUM))
    pr.num = modn ((3 * (p.x * p.x) + a))
    pr.den = modn (p.y * 2)
    pr.x = modn (modn ((pr.lam * pr.lam)) - modn (2 * p.x))
    pr.y = modn ((pr.lam * (p.x - pr.x)) - p.y)
    return pr

def suma_puntos(p, q):
    if son_iguales(p, q):
        return suma_puntos_iguales(p)
    return suma_puntos_diferentes(p, q)

def son_iguales(p,q):
    return (p.x == q.x) and (p.y == q.y)


def multiplica_k_punto(k, p):
    pr = Punto(0,0)
    pt = Punto(0,0)

    for i in range(k):
        pt = suma_puntos(p, pr)
        pr = pt

    return pr

if __name__ == "__main__":
    p_inicial = Punto(1,1)
    pt = Punto(0,0)

    mcd1 = 0
    #NUM = int(input("Número a Factorizar:"))
    k = int(input("Ingresa un valor para K:"))
    a = int(input("Ingresa un valor para A:"))
    B = a*(-1)

    #   Se Realiza la iteración desde 2 hasta k
    for i in range(2, k):
        pt = multiplica_k_punto(i, p_inicial)
        mcd1 = number.GCD(pt.den, NUM)

        if mcd1 != 1:
            print("\n\t=>  %d es un factor de %d" %(mcd1, NUM))
            q = NUM/mcd1
            print("\t=>  %d = %d*%d" %(NUM, mcd1, q))
            quit()

    print("\n\tXx No se encontro un factor de %d" %(NUM))

