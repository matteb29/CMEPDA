//questo programma è scritto in cuda c, estensione del c creato da nvidia

#include <stdio.h>

// Matrices are stored in row-major order:
// M(row, col) = *(M.elements + row * M.width + col)


//definisco una struttura matrice con attributi 
//larghezza, altezza, elementi

typedef struct {

int width;
int height;
float* elements; //puntatore a elements
//che sarà un array di valori di tipo float, ricordo che in C/C++ 
//posso usare un puntatore per indicare un array non ancora inizializzato

} Matrix;

//dato personalizzato, in cui raggruppo degli attributi,
//a differenza delle classi in python qui non ho metodi, non può contenere azioni


//una sintassi equivalente sarebbe 
//// Stile C++ (più comune)
//struct Matrix {
   // int width;
    //int height;
    //float* elements;
//};



// Thread block size
#define BLOCK_SIZE 16
//serve per definire delle costanti come se fossero private


//ricordo che __global__significa che la funzione MatMulKernel è un kernel
__global__ void MatMulKernel(const Matrix, const Matrix, Matrix);

//i primi due argomenti sono le matrici di input che definisco const cosi che la funzione
//MatMulKernel non può cambiarle, questo è necessario per sicurezza del codice e per 
//velocizzare l' accesso alla memoria da parte del compilatore (soprattutto per quest' ultimo motivo)
