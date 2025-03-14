#include <stdio.h>

int main() {
    int a = 5, b = 3;
    int resultado;

    resultado = a & b;
    printf("AND: %d\n", resultado);

    resultado = a | b;
    printf("OR: %d\n", resultado);

    resultado = a ^ b;
    printf("XOR: %d\n", resultado);

    resultado = ~a;
    printf("NOT: %d\n", resultado);

    resultado = a << 1;
    printf("Desplazamiento a la izquierda: %d\n", resultado);

    resultado = a >> 1;
    printf("Desplazamiento a la derecha: %d\n", resultado);

    return 0;
}
