#! /usr/bin/python
# -*- coding: utf-8 -*-

#   Criptografía y Seguridad
#   Proyecto 1: Crifrado de Hill

#   Autores:
#   Tadeo Guillén Diana G
#   Rivera González Damián


import numpy as np
import math
from Operaciones import *

alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # Z 26

'''
    Método que dada una palabra clave y el mensaje plano a codificar
    genera el texto codificado con la matriz de la palabra clave.
    @param clave - string de palabra clave para cifrar
    @param mensaje - string texto plano para cifrar
'''
def codificar( clave, mensaje):

    rtnCadena = ""
    #1. Construcción y verificación de la Matriz correspondiente a la clave
    matrizClave = getMatrizClave(clave)

    determinante = obtenerDeterminante(matrizClave) # Obtenemos el determinante de la matriz clave
    #print("Determinante:    "+ str(determinante))
    determinanteModular = determinante%len(alfabeto)
    #print("DeterminanteModular:    "+str(determinanteModular))
    inversoDeterminante = obtenerInverso(int(determinanteModular), len(alfabeto)) # Obtenemos el inverso en Z_26    

    #2. Construcción de n-gramas del mensaje
    matrizMensaje = getMatrizMensaje(mensaje, len(matrizClave))
    #3. Multiplicamos Matrices 
    claveXmensaje = multiplicaMatrices(matrizClave, matrizMensaje, len(alfabeto))
    #4. Recuperamos mensaje ofuscado
    rtnCadena = getMessageCipher(claveXmensaje)
    return rtnCadena


'''
    Dada la palabra clave, se genera la matriz con los índices de las letras
    de la palabra, se hace la verificación que tenga inversa en Z_26
    @param clave - string
'''
def getMatrizClave(clave):

    rtnClave = []   # arreglo vacio
    clave = str.upper(clave) # pasamos a mayúsculas la clave
    raizDouble = math.sqrt( len(clave) )
    if raizDouble == int(raizDouble):

        raizInt = int(raizDouble)
        rtnClave = np.zeros((raizInt, raizInt)) # Creamos una matriz de ceros para rellenar
        flagClave = 0

        for i in range(raizInt):
            for j in range(raizInt):
                rtnClave[i][j] = alfabeto.index(clave[flagClave]) # Guardamos el índice de la letra en la matriz
                flagClave += 1


    else:   # no es exacto la raíz cuadrada del la clave
        print("Llave invalida, no se puede formar una matriz de NxN")
        quit()

    return rtnClave



'''
    NOTA: este método regresa la matriz de manera transpuesta, es decir:
    [ 2  15 13 ]
    [ 19 21 11 ]
    en lugar de :
    [ 2 19] 
    [15 21] 
    [13 11] 
    debido a que es más fácil trabajar con la primer versión de matriz
    @param mensaje - string
    @param longitudeMatrizClave - int
    @return
    '''
def getMatrizMensaje( mensaje, longitudeMatrizClave):
    try:
        rtnMensaje = []
        mensaje = completaCadena(longitudeMatrizClave, mensaje)

        if len(mensaje) % longitudeMatrizClave == 0 :
            
            rows = len(mensaje)/longitudeMatrizClave    #length of N-gramas
            rtnMensaje = np.zeros((rows, longitudeMatrizClave)) #initializing matrix

            flagPositionMesaje = 0
            
            for i in range(rows):   # i-rows
                for j in range(longitudeMatrizClave):   #j-columns                        
                    rtnMensaje[i][j] = alfabeto.index(mensaje[flagPositionMesaje])
                    flagPositionMesaje += 1
                    
        else:
            print("Mensaje invalido, no se puede formar matrices de Nx1")
        
        return rtnMensaje
    except ValueError as ve:
        print("ERROR de caracter no identificado !")
        quit()
    


'''
    Este metodo acompleta una cadena con 'X' paraque vualquier mensaje de cualquier
    tamano pueda ser codificado a cualquier clave de cualquier tamano
    @param longitudClave es la longitud del texto de la clave
    @param mensaje es el mensaje ingresado por el usuario
    @return mensaje completado para ser codificado
'''
def completaCadena( longitudClave, mensaje):
    diferencia = len(mensaje)%longitudClave
    
    if diferencia!=0:
        #print("La diferencia es: " + str(diferencia))
        for i in range(longitudClave-diferencia):
            mensaje += "X"			
    
    return mensaje;

'''
    Método que quita los caracteres que no forman parte del alfabeto
'''
def limpiaMensaje(mensaje):
    mensajeLimpio = ""
    for item in mensaje:
        if item in alfabeto:
            mensajeLimpio+=item
    
    return mensajeLimpio



'''
    Dada la matriz con los índices del mensaje cifrado o descifrado,
    genera el texto con las letras de los índices en el alfabeto.
    @param matrizChiper - matriz con índices del mensaje
'''
def getMessageCipher(matrizChiper):
    rtnMensaje = "";

    for i in range(len(matrizChiper)):
        for j in range(len(matrizChiper[i])):
            indice = int(round(matrizChiper[i][j]))%len(alfabeto)
            rtnMensaje = rtnMensaje+(alfabeto[indice]+"") 
    
    return rtnMensaje



'''
    Método que dada la matriz de los índices de las letras de la palabra clave
    y el mensaje plano a decodificar, genera el texto plano del mensaje original
    @param matrizClave - matriz de índices de las letras de la palabra clave
    @param mansaje - string mensaje cifrado para decodificar
'''
def decodificar( matrizClave, mensaje):
    rtnCadena = ""
    #1. Obtenemos la matriz inversa de la matriz clave
    matrizInversa = obtenerMatrizInversa(matrizClave, len(alfabeto))

    #2. Construcción de n-gramas del mensaje
    matrizMensaje = getMatrizMensaje(mensaje, len(matrizClave))
    #3. Multiplicamos Matrices 
    claveXmensaje = multiplicaMatrices(matrizInversa , matrizMensaje, len(alfabeto))
    #4. Recuperamos mensaje ofuscado
    rtnCadena = getMessageCipher(claveXmensaje)
    return rtnCadena


#   Autores:
#   Tadeo Guillén Diana G
#   Rivera González Damián
if __name__ == "__main__":
    

    # INGRESO DEL TEXTO A CODIFICAR
    print("\t CIFRADO DE HILL\n")
    mensaje = raw_input("Ingresa el mensaje:    ")
    mensaje = str.upper(mensaje).replace(" ", "")
    mensaje = limpiaMensaje(mensaje)

    # INGRESO DE LA PALABRA CLAVE A CODIFICAR EL TEXTO
    clave = raw_input("Ingresa la clave:    ")
    clave = str.upper(clave).replace(" ", "")
    print("\n")

    # IMPRIMIMOS LA INFORMACIÓN
    print("Mensaje original:    "+ mensaje)
    print("Clave:               "+ clave)
    print("\n")

    # Claves en Z 26
    #FZHC
    #CBFD

    # CIFRAMOS
    mensajeCodificado = codificar(clave, mensaje)
    print("\n >>>> Mensaje codificado:     "+ mensajeCodificado)
    print("\n")
    matriz_clave = getMatrizClave(clave)

    # DESCIFRAMOS
    mensajeDecodificado = decodificar(matriz_clave, mensajeCodificado)
    print("\n <<<< Mensaje decodificado:    "+ mensajeDecodificado +"\n")