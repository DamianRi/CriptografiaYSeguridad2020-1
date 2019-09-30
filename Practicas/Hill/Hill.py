#! /usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
from numpy.linalg import inv
from numpy.linalg import det
import math

alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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

    determinante = int(round(det(matrizClave))) # Obtenemos el determinante de la matriz clave
    print("Determinante:    "+ str(determinante))
    determinanteModular = determinante%26
    print("DeterminanteModular:    "+str(determinanteModular))
    inversoDeterminante = obtenerInverso(int(determinanteModular), 26) # Obtenemos el inverso en Z_26    

    #2. Construcción de n-gramas del mensaje
    matrizMensaje = getMatrizMensaje(mensaje, len(matrizClave))
    #3. Multiplicamos Matrices 
    claveXmensaje = multiplicaMatrices(matrizClave, matrizMensaje)
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
    '''
    # Verificamos que la matriz tenga inversa en Z_26
    if int( round(det(rtnClave)%len(alfabeto))) != 1:
        print("Llave inválida, la matriz de la llave no tiene inversa en Z_26")
        quit()
    '''
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
        print("La diferencia es: " + str(diferencia))
        for i in range(longitudClave-diferencia):
            mensaje += "X"			
    
    return mensaje;
	

'''
    Dada la matriz de la palabra clave y la matriz del mensaje
    Se hace la multiplicación de ambas matrices para obtener los índices de cifrado
    @param matrizClave - matriz de índices de la palabra clave
    @param matrizMensaje - matriz de índices de las letras del mensaje
'''
def multiplicaMatrices(matrizClave, matrizMensaje):
    '''
    rtnMultiplicacion = np.zeros((len(matrizClave), len(matrizMensaje) ) )
    for h in range(len(rtnMultiplicacion)):
        for i in range(len(matrizClave)):
            a = 0
            for j in range(len(matrizMensaje)):
                a = a + (matrizClave[i][j]*matrizMensaje[i][j])

            rtnMultiplicacion[h][i] = a % len(alfabeto)

    return rtnMultiplicacion
    '''    
    rtnMultiplicacion = np.matmul(matrizMensaje, matrizClave)%len(alfabeto)
    return rtnMultiplicacion
    

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
    Método que obtiene el número inverso de a modulo m
'''
def obtenerInverso(a,m):

    c1 = 1
    c2 = -(m/a) #coeficiente de a y b respectivamente
    t1 = 0
    t2 = 1 #coeficientes penultima corrida
    r = m % a #residuo, asignamos 1 como condicion de entrada 
    x=a
    y=r
    c = 0
    while r !=0:
    
        c = x/y #cociente
        r = x%y #residuo
        #guardamos valores temporales de los coeficientes
        #multiplicamos los coeficiente por -1*cociente de la division
        c1*=-c
        c2*=-c
        #sumamos la corrida anterior
        c1+=t1
        c2+=t2
        #actualizamos corrida anterior
        t1=-(c1-t1)/c
        t2=-(c2-t2)/c
        x=y
        y=r
    
    if x==1: #//residuo anterior es 1 , son primos relativos y el inverso existe
        print("Existe Inverso: "+str(int(t2%26)))
        return int(t2%26)
        
    else:
        print("El determinante no tiene inverso en Z 26 !")
        quit()


'''
    Método que dada la matriz de los índices de las letras de la palabra clave
    y el mensaje plano a decodificar, genera el texto plano del mensaje original
    @param matrizClave - matriz de índices de las letras de la palabra clave
    @param mansaje - string mensaje cifrado para decodificar
'''
def decodificar( matrizClave, mensaje):
    rtnCadena = ""
    #1. Obtenemos la matriz inversa de la matriz clave
    #matrizInversa = inv(matrizClave)%len(alfabeto)
    print("Matriz Clave")
    print(matrizClave)

    inversa = np.linalg.inv(matrizClave) # Obtenemos la inversa de la matriz clave

    determinante = int(round(det(matrizClave))) # Obtenemos el determinante de la matriz clave
    print("Determinante:    "+ str(determinante))

    determinanteModular = determinante%26
    print("DeterminanteModular:    "+str(determinanteModular))
    
    inversoDeterminante = obtenerInverso(int(determinanteModular), 26) # Obtenemos el inverso en Z_26
    print("InversoModular:     "+ str(inversoDeterminante))
    
    inversa = determinante * inversa
    print(inversa)
    matrizInversa = inversoDeterminante * inversa
    
    #2. Construcción de n-gramas del mensaje
    matrizMensaje = getMatrizMensaje(mensaje, len(matrizClave))
    #3. Multiplicamos Matrices 
    claveXmensaje = multiplicaMatrices(matrizInversa, matrizMensaje)
    #4. Recuperamos mensaje ofuscado
    rtnCadena = getMessageCipher(claveXmensaje)
    return rtnCadena








# INGRESO DEL TEXTO A CODIFICAR
mensaje = raw_input("Ingresa el mensaje:    ")
mensaje = str.upper(mensaje).replace(" ", "")


# INGRESO DE LA PALABRA CLAVE A CODIFICAR EL TEXTO
clave = raw_input("Ingresa la clave:    ")
clave = str.upper(clave).replace(" ", "")
print("\n")

# IMPRIMIMOS LA INFORMACIÓN
print("Mensaje original:    "+ mensaje)
print("Clave:               "+ clave)
print("\n")


#FZHC
#CBFD

# CIFRAMOS
mensajeCodificado = codificar(clave, mensaje)
print("\n >>>> Mensaje codificado:     "+ mensajeCodificado)
print("\n")
matriz_clave = getMatrizClave(clave)

# DESCIFRAMOS
mensajeDecodificado = decodificar(matriz_clave, mensajeCodificado)
print("\n <<<< Mensaje decodificado:    "+ mensajeDecodificado)