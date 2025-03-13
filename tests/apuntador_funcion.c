#include <stdio.h>

void imprimirNumero(int *num) {
    printf("El número es: %d\n", *num);
}

int main() {
    int numero = 50;
    int *puntero = &numero;

    imprimirNumero(puntero);

    return 0;
}
