int a = 42;
int n = 10; //dimensione dei vettori

//creo due array nella cpu cioè nell' host
float x[n], y[n];


// fill x, y
cublasInit(); //inizializziamo la libreria CUBLAS 
//obliggatorio per chiamata a routine GPU 

//alloco memoria nella GPU usando due puntatori a celle di memoria della GPU
float * d_x, * d_y;
//d_ è una convenziare per dichiarare puntatori a memoria della GPU

//cudaMalloc serve per allocare memoria sulla GPU: cioè riservo dello spazio di memoria nella GPU
//per copiare i dati che ricevo dall' host

cudaMalloc((void **)&d_x, n * sizeof(x[0]);
//void** è un puntatore al puntatore *d_x che voglio inizializzare 
//io passo alla funzione malloc l' indirizzo di memoria del puntatore così che ottengo l' indirizzo di 
//memoria del puntatore con il quale lavorerò


cudaMalloc((void **)&d_y, n * sizeof(y[0]);


//cublasSetVector copia i dati dall’host (x, y) al device (d_x, d_y).
cublasSetVector(n, sizeof(x[0]), x, 1, d_x, 1);
cublasSetVector(n, sizeof(y[0]), y, 1, d_y, 1);

//1 significa che nell' array x deve copiare tutti gli elementi consecuti, se fosse 2 vorrebbe dire che copia
//solo ogni due elementi dell' array cioè uno si e uno no
//d_x[i⋅dstStride] = x[i⋅srcStride] (per i=0..n−1)

//srcStride = stride sorgente
//dstStride = stride destinazione
//Lo stride è la distanza in memoria tra un elemento e il successivo quando si accede a un array o vettore.



//Dopo questa chiamata, d_y[i] = a*d_x[i] + d_y[i].
cublasSaxpy(n, a, d_x, 1, d_y, 1);
//eseguo saxpy



cublasGetVector(n, sizeof(y[0]), d_y, 1, y, 1);
//copia i dati d_y dalla GPU alla CPU

cublasShutdown();
//libera risorse dalla libreria cublas