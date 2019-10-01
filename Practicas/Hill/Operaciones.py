#! /usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import math

'''
    Dada la matriz de la palabra clave y la matriz del mensaje
    Se hace la multiplicación de ambas matrices para obtener los índices de cifrado
    @param matrizClave - matriz de índices de la palabra clave
    @param matrizMensaje - matriz de índices de las letras del mensaje
'''
def multiplicaMatrices(matrizClave, matrizMensaje, modulo):
    '''
    print("Matriz Clave")
    print(matrizClave)

    print("Matriz Mensaje")
    print(matrizMensaje)
    '''


    rtnMultiplicacion = np.zeros((len(matrizMensaje), len(matrizClave) ) )
    
    for h in range(len(rtnMultiplicacion)):
        for i in range(len(matrizClave)):
            a = 0
            for j in range(len(matrizMensaje[0])):
                #print(str(matrizClave[j][i])+" - "+str(matrizMensaje[h][j]))
                a = a + (matrizClave[j][i]*matrizMensaje[h][j])

            rtnMultiplicacion[h][i] = a % modulo

    '''
    print("Matriz multiplicada A Mano")
    print(rtnMultiplicacion)

    rtnMultiplicacion2 = np.matmul(matrizMensaje, matrizClave)%modulo
    print("Multiplicación Python")
    print(rtnMultiplicacion2)
    '''
    return rtnMultiplicacion


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
        #print("Existe Inverso: "+str(int(t2%m)))
        return int(t2%m)
        
    else:
        print("El determinante no tiene inverso en Z "+str(m)+"!")
        quit()



'''
    Método para obtener el determinante de una matriz
'''
def obtenerDeterminante(matriz):
    det = 0
    if len(matriz) == 2:
        det = (matriz[0][0]* matriz[1][1] - matriz[0][1]* matriz[1][0])

    for i in range(len(matriz)):
        nuevaMatriz = np.zeros((len(matriz)-1, len(matriz)-1) )
        
        for j in range(len(matriz)):
            
            if(j != i):

                for k in range(len(matriz)):
                    
                    indice = -1
                    if j < i:
                        indice = j
                    else:
                        indice = j-1


                    nuevaMatriz[indice][k-1] = matriz[j][k]


        if i%2 == 0:
            det = det + (matriz[i][0] * obtenerDeterminante(nuevaMatriz))
        else:
            det = det - (matriz[i][0] * obtenerDeterminante(nuevaMatriz))


    #print("Determinante Obtenido "+str(int(det)))
    return int(det)


'''
    Método para obtener la matriz inversa de la matriz
'''
def obtenerMatrizInversa(matriz, modulo):
    det = obtenerDeterminante(matriz)%modulo
    mod = modulo
    inverso = obtenerInverso(det, mod)

    matriz_inversa = obtenerMatrizCofactores(matriz)
    matriz_inversa = np.transpose(matriz_inversa)    
    matriz_inversa = matriz_inversa*inverso

    for i in range(len(matriz_inversa)):
        for j in range(len(matriz_inversa)):
            matriz_inversa[i][j] = matriz_inversa[i][j]%mod
    
    for i in range(len(matriz_inversa)):
        for j in range(len(matriz_inversa)):
            if matriz_inversa[i][j] < 0:
                matriz_inversa[i][j] = matriz_inversa[i][j] + mod


    return matriz_inversa


'''
    Método para obtener los cofactores de una matriz
'''
def obtenerMatrizCofactores(matriz):
    
    nuevaMatriz = np.zeros((len(matriz), len(matriz)))

    if len(matriz) == 2:
        nuevaMatriz[0][0] = matriz[1][1]
        nuevaMatriz[0][1] = -matriz[1][0]
        nuevaMatriz[1][0] = -matriz[0][1]
        nuevaMatriz[1][1] = matriz[0][0]
        return nuevaMatriz

    for i in range(len(matriz)):
        for j in range(len(matriz)):
            
            det = np.zeros((len(matriz)-1, len(matriz)-1))
            for k in range(len(matriz)):
                if(k != i):
                    for l in range(len(matriz)):
                        if l != j:
                            if k < i:
                                indice1 = k
                            else:
                                indice1 = k-1
                            
                            if l < j:
                                indice2 = l
                            else:
                                indice2 = l-1
                            
                            det[indice1][indice2] = matriz[k][l]


            detValor = obtenerDeterminante(det)
            nuevaMatriz[i][j] = int(detValor * (pow(-1, i+j+2)))
    return nuevaMatriz
