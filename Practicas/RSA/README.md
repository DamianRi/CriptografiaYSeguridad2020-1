## Criptografía y Seguridad
## Proyecto 2: RSA

Autores:
- Tadeo Guillén Diana G
- Rivera González Damián

- - -
Nota: Código implementado con Python 3.7.5

Dependencias:

Se debe tener instalado el paquete **PyCryptodome**, si se tiene configurado Python 3 de manera adecuada en la computadora y teniendo instalado Pip 3, es suficiente con ejecutar el siguiente comando para descargar el paquete:
```
    $ pip3 install pycryptodome
```
De otra manera se deja el enlace para su instalación [**PyCryptodome**](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)

- - -

### Descripción
Implementación del cifrado RSA (Rivest, Shamir y Adleman). Lo valores del p y q tienen una longitud de 100 dígitos.

### Contenido
-   [RSA](/)
    - [src](src/)
       - [RSA.py](src/RSA.py)
    - [README.md](README.md)

### Ejecución 
Dentro de una terminal, estar colocado dentro de la carpeta **[src](src/)**, y ejecutar el siguiente comando:
```
    ...RSA/src$ python3 RSA.py
```
Una vez que se inicializan los valores de una instancia de _RSA_ se debe introducir una cadena como entrada, para mostrar su cifrado y decifrado con esta implementación