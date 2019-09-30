import java.math.*;
import java.util.Scanner;

public class Hill {

    static String alfabetoMayusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; 
    static int[][] mClave;
    static int[][] mClaveInversa;
    static int alfabeto;
    static int[][] matrizMensajeStatic;
    /**
     * 
     */
    private static String codificar(String clave, String mensaje) {
        String rtnCadena = "";
        //1. Construcción y verificación de la Matriz correspondiente a la clave
        int[][] matrizClave = getMatrizClave(clave);
        mClave = matrizClave; // Guardamos la matriz clave de forma estática
        alfabeto = alfabetoMayusculas.length();
        //2. Construcción de n-gramas del mensaje
        int[][] matrizMensaje = getMatrizMensaje(mensaje, matrizClave.length);
        matrizMensajeStatic = matrizMensaje;    //Guardamos las matriz del mensaje cifrado
        //3. Multiplicamos Matrices 
        int [][] claveXmensaje = multiplicaMatrices(matrizClave, matrizMensaje);

        //4. Recuperamos mensaje ofuscado
        rtnCadena = getMessageCipher(claveXmensaje);

        return rtnCadena;
    }

    /**
     * 
     * @param clave
     * @return
     */
    private static int[][] getMatrizClave(String clave){
        int[][] rtnClave = new int[0][0];

        double raizDouble = Math.sqrt( clave.length() );
        if (raizDouble == (int)raizDouble){

            int raizInt = (int)raizDouble;
            rtnClave = new int[raizInt][raizInt];
            int flagClave = 0;
            for(int i=0; i<raizInt; i++){
                for(int j=0; j<raizInt; j++){
                    rtnClave[i][j] = alfabetoMayusculas.indexOf(clave.charAt(flagClave));
                    flagClave++;
                }
            }

        }
        else{ //no es exacto la raíz cuadrada del la clave
            System.out.println("Llave invalida, no se puede formar una matriz de NxN");
            // rtnClave[i][j] = null;
        }

        return rtnClave;
    }

    /**
     * NOTA: este método regresa la matriz de manera transpuesta, es decir:
     * [ 2  15 13 ]
     * [ 19 21 11 ]
     * en lugar de :
     * [ 2 19] 
     * [15 21] 
     * [13 11] 
     * debido a que es más fácil trabajar con la primer versión de matriz y 
     * por el mismo diseño del lenguaje Java.
     * @param mensaje
     * @return
     */
    private static int[][] getMatrizMensaje(String mensaje, int longitudeMatrizClave){
        int[][] rtnMensaje = new int[0][0];
		mensaje=completaCadena(longitudeMatrizClave, mensaje);
        if( mensaje.length()%longitudeMatrizClave == 0 ){
			
            int rows = mensaje.length()/longitudeMatrizClave; //length of N-gramas
            rtnMensaje = new int[rows][longitudeMatrizClave]; //initializing matrix

            int flagPositionMesaje = 0;
            for(int i=0; i<rows; i++){ // i-rows
                for(int j=0; j<longitudeMatrizClave; j++){ // j-columns
                    rtnMensaje[i][j] = alfabetoMayusculas.indexOf(mensaje.charAt(flagPositionMesaje));
                    flagPositionMesaje++;
                    System.out.print(rtnMensaje[i][j]+" ");
                }
                System.out.print("\n");

            }

        }else{
            System.out.println("Mensaje invalido, no se puede formar matrices de Nx1");
        }

        return rtnMensaje;
    }
    
    /**
     * Este metodo acompleta una cadena con 'X' paraque vualquier mensaje de cualquier
     * tamano pueda ser codificado a cualquier clave de cualquier tamano
     * @param longitudClave es la longitud del texto de la clave
     * @param mensaje es el mensaje ingresado por el usuario
     * @return mensaje completado para ser codificado
     */
    private static String completaCadena(int longitudClave, String mensaje){
		int diferencia=mensaje.length()%longitudClave;
		if( diferencia != 0){
			System.out.println("La diferencia es:            " + diferencia);
			for(int i =0;i<(longitudClave-diferencia);i++){
				mensaje+="X";
			}
			
		}
		return mensaje;
	}

    /**
     * 
     * @param matrizClave
     * @param matrizMensaje
     * @return Matriz con operaciónes resueltas y el modulo calculado en cada posición.
     */
    private static int[][] multiplicaMatrices(int[][] matrizClave, int[][] matrizMensaje){
        int[][] rtnMultiplicacion = new int[matrizMensaje.length][matrizMensaje[0].length];
        
        for(int h=0; h<rtnMultiplicacion.length;h++){
            for(int i=0; i<matrizClave.length; i++){ // looping on rows of matrizMensaje
                int a = 0;
                for(int j=0; j<matrizMensaje[0].length; j++){
                    a = a + (matrizClave[i][j]*matrizMensaje[h][j]);
                }
                rtnMultiplicacion[h][i] = a % alfabetoMayusculas.length();
            }
        }

        return rtnMultiplicacion;
    }

    /**
     * 
     * @param matrizChiper
     * @return
     */
    private static String getMessageCipher(int[][] matrizChiper){
        String rtnMensaje = "";

        for(int i=0; i<matrizChiper.length; i++){
            for(int j=0; j<matrizChiper[i].length; j++){
                rtnMensaje = rtnMensaje + ( alfabetoMayusculas.charAt(matrizChiper[i][j]) + "");
            }
        }

        return rtnMensaje;
    }
    

    /**
     * Obtiene la matriz inversa de una matriz dentro de un Z_n
     * @param matriz - matriz de enteros
     * @param n - dimensión de Z_n
     */
    private static int[][] obtenerInversa(int[][] matriz, int n){  
        int det = Determinante.determinante(matriz);
        int[][] inversa;
        System.out.println("Tiene inversa?:"+ det%n);
        if (det%alfabeto != 1) {    // Verificamos sí la matriz tiene determinante
            System.out.println("LA MATRIZ NO TIENE INVERSA");
            return new int[0][0]; 
        }else{
            //inversa = (int[][])Inverse.invert( (double[][]) matriz );
        }
        //mClaveInversa = inversa;
        return mClaveInversa;
    }

    /**
     * 
     */
    private static String decodificar(String cadena, int[][] llave) {
        String rtnCadena = "";

        //3. Multiplicamos Matrices 
        int [][] claveXmensaje = multiplicaMatrices(mClaveInversa, matrizMensajeStatic);

        //4. Recuperamos mensaje ofuscado
        rtnCadena = getMessageCipher(claveXmensaje);

        return rtnCadena;

    }


    /**
     * Método principal
     */
    public static void main(String[] args) {

		Scanner input = new Scanner(System.in);
		System.out.println("Igresa el mensaje ");
		String mensaje = input.nextLine().toUpperCase().replaceAll(" ","");
		
		System.out.println("Igresa la clave ");
		String clave = input.nextLine().toUpperCase().replaceAll(" ","");

        // 1. Mensaje original
		System.out.println("Mensaje original: " + mensaje);
		System.out.println("Clave:            " + clave);
        System.out.println();  

        // 2. Codificar
        String mensajeCodificado = codificar(clave, mensaje);
        System.out.println("Mensaje codificado:   " + mensajeCodificado);
        //obtenerInversa(mClave, alfabeto);
        // 3. Decodificar
        //String cadenaDecodificada = decodificar(mensajeCodificado, mClaveInversa); 
        //System.out.println("Texto decodificado: " + cadenaDecodificada); 
    }

}
