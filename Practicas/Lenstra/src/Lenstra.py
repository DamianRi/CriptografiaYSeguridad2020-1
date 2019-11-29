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

Ejecución: 
$   python3 Lenstra.py
- - -
"""
from Crypto.Util import number
import random
import math

NUM = 87463 # Número por defecto a factorizar

"""
    Clase para la representación de un Punto,
    son lo objetos con los que se trabaja para el cálculo 
    de la factorización del número
"""
class Punto:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.num = 0    # num: numerador del valor de lambda
        self.den = 0    # den: denominador del valor de lambda
        self.lam = 0    # lam: valor del lambda

"""
    Función para realzar la suma entre dos Puntos diferentes
"""
def suma_puntos_diferentes(p, q):
    pr = Punto(0,0) # Punto para regresar el resultado de la suma de p y q

    if p.x == 0 and p.y == 0:
        return q
    if q.x == 0 and q.y == 0:
        return p
    if (p.x == q.x) and (q.x == (-1*p.y)):
        return pr

    #pr.lam = ((q.y-p.y)*number.inverse(q.x - p.x, NUM)) % NUM
    pr.num = (q.y - p.y) % NUM
    pr.den = (q.x - p.x) % NUM
    pr.lam = pr.num * number.inverse(pr.den, NUM) % NUM
    
    #
    #   x_3 = lam^2 - x_1 - x_2 mod N
    #
    pr.x = (math.pow(pr.lam, 2) - p.x - q.x) % NUM
    #
    #   y_3 = lam(x_1 - x_3) - y_1 mod N
    #
    pr.y = ((pr.lam * (p.x - pr.x)) - p.y) % NUM

    return pr

"""
    Función para realizar la suma entre dos Puntos iguales
"""
def suma_puntos_iguales(p):
    pr = Punto(0,0) # Punto para regresar el resultado de la suma de p y q
    
    pr.num = ((3 * (math.pow(p.x, 2))) + a) % NUM
    pr.den = (2 * p.y)
    pr.lam = (pr.num * number.inverse(pr.den, NUM)) % NUM

    #
    #   x_3 = lam^2 - (2*x_1)  mod N
    #
    pr.x = (math.pow(pr.lam, 2) - (2 * p.x)) % NUM
    #
    #   y_3 = lam(x_1 - x_3) - y_1 mod N
    #
    pr.y = ((pr.lam * (p.x - pr.x)) - p.y) % NUM
    
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
    pr = Punto(0,0) # Punto para regresar el resultado del kP
    pt = Punto(0,0) # Punto temporal para el calculo de las iteraciones

    for i in range(k):
        pt = suma_puntos(p, pr)
        pr = pt

    return pr


if __name__ == "__main__":

    print("\n\t --- FACTORIZACIÓN POR ALGORITMO DE LENSTRA ---")
    NUM = input("\nIngresa un número a Factorizar (o enter para un random):")
    # Manejo de entrada para un N aleatroio
    if NUM == "":
        p = number.getPrime(12)
        q = number.getPrime(12)
        NUM = p*q
        print(p, q)
    else:
        NUM = int(NUM)
    
    print("N = ", NUM)

    k = input("Número máximo de iteraciones K (o enter para k por defecto): ")
    # Manejo de entrada para una cantidad K de iteraciones 
    if k == "":
        cad = '{:<0'+str(len(str(NUM)))+'d}'
        k = int(cad.format(1))
    else:
        k = int(k)

    print("K =",k)

    a = random.randrange(1, NUM)    # coeficiente 'a' aleatorio de la curva
    B = a*(-1)  # Coeficiente 'B' de la curva

    # Un punto no trivial en la curva
    p_inicial = Punto(1,1)
    pt = Punto(0,0) # Punto temporal para las operaciones

    print("Curva Elíptica: y^2 = x^3 +"+str(a)+"x + ("+str(B)+")")

    mcd = 0
    #   Se Realiza la iteración desde a=2 hasta k
    for a in range(2, k):
        pt = multiplica_k_punto(a, p_inicial)   # Calculamos kP

        # Obtenemos el máximo común divisor
        mcd = number.GCD(pt.den, NUM)
        if mcd != 1:    # Si el denominador de lambda no tiene inverso en Z_NUM
            print("\n\t=>  p = %d es un factor de %d" %(mcd, NUM))
            q = NUM/mcd
            print("\t=>  N = %d = %d*%d = p*q\n" %(NUM, mcd, q))
            quit()

    print("\n\tXx No se encontro un factor de %d con las %d iteraciones" %(NUM, k))
