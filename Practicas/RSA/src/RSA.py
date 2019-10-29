#! /usr/bin/env python3
#-*- coding: utf-8 -*-

'''
Nota: Código implementado con Python 3.7.5

Dependencias:

Se debe tener instalado el paquete **PyCryptodome**, si se tiene configurado Python 3 de manera adecuada en la computadora y teniendo instalado Pip 3, es suficiente con ejecutar el siguiente comando para descargar el paquete:
```
    $ pip3 install pycryptodome
```
De otra manera se deja el enlace para su instalación [**PyCryptodome**](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)
'''


from Crypto.Util import number

class RSA():

    def __init__(self):
        print("\tINICIALIZANDO VALORES DE RSA")
        #   1. Dos números primos aleatorios
        #self.p = number.getStrongPrime(512)
        #self.q = number.getStrongPrime(512)
        self.p = number.getPrime(330)
        self.q = number.getPrime(330)

        #   2. Se calcula n = p*q
        self.n = self.p*self.q
        
        #   3. Se calcula la función de Euler
        #   Phi(n) = (p-1)(q-1)
        self.phi = (self.p-1)*(self.q-1)

        #   4. Entero positivo 'e' menor que 'phi' y que sea coprimo con 'phi'
        #self.e = number.getPrime(128)
        self.e = self.phi-2
        g = number.GCD(self.e, self.phi)
        while not g == 1 :
            #self.e += 1
            self.e -= 1
            g = number.GCD(self.e, self.phi)

        #   5. Se determina 'd' que satisfaga la congruencia e*d = 1 (mod Phi(n))
        self.d = number.inverse(self.e, self.phi)

    '''
        Función que codifica el mensaje que recibe como parametro
    '''
    def codificar(self, mensaje):
        print("\n\t<<<<<    CODIFICANDO MENSAJE:\n\t", mensaje)
        #   Se toma cada caracter del mensaje y se codifica con la llave publica
        #   C = m ^ e (mod n)
        mensaje_codificado = [expo_bin_modular(ord(char), self.e, self.n) for char in mensaje]
        # Regresa la lista con los numeros que representan a cada caracter del mensaje
        return mensaje_codificado        

    '''
        Función que decodifica el mensaje que recibe como parametro
    '''
    def decodificar(self, mensaje):
        print("\n\t<<<<<    DECODIFICANDO MENSAJE:\n\t", mensaje)
        #   Se toma cada numero en la lista del mensaje_codificado y se decodifica con la llave privada
        #   M = c ^ d (mod n)
        mensaje_decodificado = [chr(expo_bin_modular(char, self.d, self.n)) for char in mensaje]
        # Regresa la cadena formada por los caracteres de la lista
        return ''.join(mensaje_decodificado)        

"""
    Funcion que realiza exponenciacion binaria y modular
"""
def expo_bin_modular(a, b, m):
    r = 1
    while (b):
        if (b & 1):
            r = (r * a) % m
        b >>= 1
        a = ((a % m) * (a % m)) % m
    return r

"""
Integrantes:
    Tadeo Guillén Diana G
    Rivera González Damián
"""
if __name__ == '__main__':
    
    RSA = RSA()
    mensaje = input("\tINGRESA UN MENSAJE: ")
    m_codificado = RSA.codificar(mensaje)
    print("\n\t>>>>>  MENSAJE CODIFICADO:\n\t", m_codificado)
    m_decodificado = RSA.decodificar(m_codificado)
    print("\n\t>>>>>  MENSAJE DECOFICADO:\n\t", m_decodificado)
