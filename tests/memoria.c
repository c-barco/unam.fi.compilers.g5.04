#include <stdio.h>
#include <stdlib.h>

int main() {
    int *ptr = (int*) malloc(5 * sizeof(int));

    if (ptr == NULL) {
        printf("Error al asignar memoria.\n");
        return 1;
    }

    for (int i = 0; i < 5; i++) {
        ptr[i] = i * 2;
        printf("Valor en ptr[%d] = %d\n", i, ptr[i]);
    }

    free(ptr);
    return 0;
}
