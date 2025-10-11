
//__global__ è una indicazione al compilatore per indicare che la funzione
//saxpy_cuda è un kernel: il kernel viene eseguito dalla GPU ma la chiamata di esecuzione è gestita dalla CPU

__global__ void saxpy_cuda(int n, float a, float * x, float * y) {

//CUDA organizza i thread in blocchi e griglie
//blockDim è la dimensione del blocco cioè quanti thread ci sono nel blocco
//blockIDx è l' indice del blocco in esecuzione all' interno della griglia 
//threadIdx è l' indice del thread in esecuzione nel  blocco

int i = blockIdx.x * blockDim.x + threadIdx.x;

//alla fine i è l' indice globale del thread in esecuzione (la posizione del thread all' interno della griglia)
//quindi questa è una formula per sapere quale è l' indice globale del thread

//con n lunghezza del vettore
if (i < n)
{
    y[i] = a * x[i] + y[i];
    //ricorda che in c/c++ array e puntatori sono strettamente collegati
    //quindi y[i] si può anche scrivere come *(y+i)
}


}

int main(){


int a = 42;
int n = 10;
float x[n], y[n];

// fill x, y

for (i = 0; i < 10; i++){
    x[i] = 5;
    y[i] = 3;
}


cudaMallocManaged(&x, n * sizeof(float));
cudaMallocManaged(&y, n * sizeof(float));

//managed alloca memoria condivisa sia da CPU che da GPU così
//non serve passare dati tra host e device

saxpy_cuda<<<2,5>>>(n, a, x, y);
//<<<2,5>>> significa di eseguire il kernel saxpy_cuda con 2 blocchi, 5 thread per blocco

cudaDeviceSynchronize();
//aspetta che la GPU finisca di lavorare prima che la CPU faccia altro
//fa la sincronizzazione dei tempi tra device e host


return 0;
}