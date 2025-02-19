import java.util.Arrays;
import java.util.Scanner;

public class Main {
    
    public static boolean puedenColocarVacas(int[] establos, int N, int C, int dist) {
        int cantidad = 1;
        int ultimaPosicion = establos[0];
        
        for (int i = 1; i < N; i++) {
            if (establos[i] - ultimaPosicion >= dist) {
                cantidad++;
                ultimaPosicion = establos[i];
            }
            if (cantidad == C) {
                return true;
            }
        }
        return false;
    }
    
    public static int encontrarDistanciaMaxima(int[] establos, int N, int C, int bajo, int alto) {
        if (bajo > alto) {
            return alto;
        }
        
        int medio = (bajo + alto) / 2;
        
        if (puedenColocarVacas(establos, N, C, medio)) {
            return encontrarDistanciaMaxima(establos, N, C, medio + 1, alto);
        } else {
            return encontrarDistanciaMaxima(establos, N, C, bajo, medio - 1);
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt();
        
        while (t-- > 0) {
            int N = sc.nextInt();
            int C = sc.nextInt();
            int[] establos = new int[N];
            
            for (int i = 0; i < N; i++) {
                establos[i] = sc.nextInt();
            }
            
            Arrays.sort(establos);
            
            int bajo = 1;
            int alto = establos[N-1] - establos[0];
            
            int resultado = encontrarDistanciaMaxima(establos, N, C, bajo, alto);
            System.out.println(resultado);
        }
        
        sc.close();
    }
}




