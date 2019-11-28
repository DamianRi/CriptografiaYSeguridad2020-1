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
import random
import sys
import math
import time

NUM = 87463 # Número por defecto a factorizar

class Punto:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lam = 0
        self.num = 0
        self.den = 0

def modn(x):
    return (x+NUM)%NUM

"""
    Función para realzar la suma entre dos Puntos diferentes
"""
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
    pr.den = modn(q.x - p.x)
    pr.x = modn (modn (pr.lam * pr.lam) + modn ((-1 * p.x)) + modn ((-1 * q.x)))
    pr.y = modn ((pr.lam * (p.x - pr.x)) - p.y)
    return pr

"""
    Función para realizar la suma entre dos Puntos iguales
"""
def suma_puntos_iguales(p):
    pr = Punto(0,0)
    pr.lam = modn (((3 * (p.x * p.x)) + a) * number.inverse(p.y * 2, NUM))
    pr.num = modn ((3 * (p.x * p.x) + a))
    pr.den = modn (p.y * 2)
    pr.x = modn (modn ((pr.lam * pr.lam)) - modn (2 * p.x))
    pr.y = modn ((pr.lam * (p.x - pr.x)) - p.y)
    return pr

"""
    Función para hacer la suma de puntos
    Dados dos puntos p y q realiza la suma de estos
"""
def suma_puntos(p, q):
    if son_iguales(p, q):
        return suma_puntos_iguales(p)
    return suma_puntos_diferentes(p, q)

"""
    Función auxiliar para verificar si los puntos son iguales
"""
def son_iguales(p,q):
    return (p.x == q.x) and (p.y == q.y)

"""
    Función para realizar k veces la suma de un punto p
"""
def multiplica_k_punto(k, p):
    pr = Punto(0,0)
    pt = Punto(0,0)

    for i in range(k):
        pt = suma_puntos(p, pr)
        pr = pt

    return pr


if __name__ == "__main__":

    NUM = input("Ingresa un número a Factorizar (o enter para un random):")
    """
    """
    if NUM == "":
        p = number.getPrime(13)
        q = number.getPrime(13)
        NUM = p*q
    else:
        NUM = int(NUM)
    
    #print("p=", p, "| q=", q)
    print("N = ", NUM)
    k = input("Número máximo de iteraciones K (o enter para k por defecto): ")
    if k == "":
        cad = '{:<0'+str(len(str(NUM)))+'d}'
        k = int(cad.format(1))
    else:
        k = int(k)
    print("K =",k)

    #a = int(input("Ingresa un valor para A:"))
    a = random.randrange(1, NUM)
    B = a*(-1)

    # Un punto no trivial en la curva
    p_inicial = Punto(1,1)
    pt = Punto(0,0)

    print("Curva Elíptica: y^2 = x^3 +"+str(a)+"x + ("+str(B)+")")

    start_time = time.time()
    mcd = 0
    #   Se Realiza la iteración desde a=2 hasta k
    for a in range(2, k):
        pt = multiplica_k_punto(a, p_inicial)   # Calculamos kP

        # Obtenemos el máximo común divisor
        mcd = number.GCD(pt.den, NUM)
        if mcd != 1:    # Si no son primos
            print("\n\t=>  p = %d es un factor de %d" %(mcd, NUM))
            q = NUM/mcd
            print("\t=>  N = %d = %d*%d = p*q" %(NUM, mcd, q))
            print("\n--- %s seconds ---" % (time.time() - start_time))
            quit()

    print("\n\tXx No se encontro un factor de %d con las %d iteraciones" %(NUM, k))

main()