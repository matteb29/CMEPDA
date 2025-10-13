#include "MatrixMultiplication_global.h"

// Matrix multiplication - Host code
// Matrix dimensions are assumed to be multiples of BLOCK_SIZE



//codice da far rannare alla cpu dove gestisco allocazione della memoria nella GPU,
//copia dei dati da cpu a GPU, chiamata del kernel e copia dei risultati da GPU a CPU

void MatMul(const Matrix A, const Matrix B, Matrix C) {

  //le matrici Matrix A, B le definisco come const, per ottimizzare i tempi
  //e proteggere il codice

  // Load A and B to device memory



  //1° compito della CPU: devo copiare i dati dall' host(CPU) al device(GPU)
  //ricorda notazione d_variabile indica che la variabile è della GPU


  Matrix d_A; //definisco una matrice d_A che sarà la matrice della GPU sulla quale farò i calcoli
  //ne copio larghezza e altezza dalle matrici definite sulla CPU che sono date in input dalla funzione MatMul

  d_A.width = A.width; //qui copio la variabile A.widht della CPU in una variabile d_A.widht
  //che sarà importata nella GPU come d_A.width
  //ricordo che width, height sono attributi della struttura quindi si dichiarano come  variabile.attributo

  d_A.height = A.height;

  
  // 2° compito della CPU: devo allocare memoria nella GPU


  size_t size = A.width * A.height * sizeof(float); //questa variabile è utilizzata
  //per definire quanta memoria devo allocare, so che ogni elemento delle matrici è un float che 
  //avrà un peso definito da sizeof(float). Dovendo allocare memoria per una matrice di dimensioni A.width, A.height
  //allora avrò un numero di elementi pari a (A.width * A.height)
  //segue che la formula per definire quanta memoria allocare non puà che essere questa soprariportata

  //devo allocare memoria nella GPU, la memoria dove la alloco?
  //la alloco in uno spazio che parte con l' indirizzo del primo elemento del vettore d_A.elements. 
  //(infatti la notazione &d_A.elements restituisce il puntatore al primo elemento , ricordo che in header
  //avevo definito float* elements come attributo di Matrix)
  //La quantià di memoria che devo allocare dipende da quanti elementi (che sono tipo float) contiene A 
  //da qui la formula per size sopra definita

  //siccome il puntatore d_A.elements in quanto puntatore si può pensare come un indirizzo di memoria allora
  //posso vedere &d_A.elements come un puntatore ad un indirizzo di memoria
  //cioè usarlo nella funzione cudaMalloc significa dire/puntare a cudaMalloc da dove iniziare ad allocare memoria

  cudaError_t err = cudaMalloc(&d_A.elements, size);

  //ricordo la sintassi di cudaMalloc:
  //cudaError_t cudaMalloc(void** devPtr, size_t size);
  //devPtr → deve essere un array/puntatore così che void** è un array/puntatore a array/puntatore
  //size → quantità di memoria da allocare, in byte
  //inoltre la funzione cudaMalloc ritorna un codice di errore (cudaSuccess se tutto OK, cudaSuccess è un tipo speciale
  //di variabile che si chiama variabile di tipo cudaError_t )
  //quindi la variabile err (di tipo  cudaError_t ) sarà uguale a cudaSucces se l' allocazione in memoria è riuscita 
  // oppure cudaErrorMemoryAllocation se memoria esaurita

  printf("CUDA malloc A: %s\n", cudaGetErrorString(err));

  //qui stampo un messaggio per capire se l' allocazione di memoria è riuscita o meno, 
  //in particolare cudaGetErrorString è una funzione di cuda che servere per leggere variabili di tipo cudaError_t
  //un semplice printf(err) mi darebbe errore
  //cudaGetErrorString(err) è quindi l' unico modo per leggere err








  //dopo aver allocato memoria sono pronto per copiare la matrice A dalla CPU alla GPU,
  //lo faccio tramite il comando cudaMemcpy che serve a copiare dati tra memoria host (CPU) e device (GPU) (in entrambi i sensi
  //c' è l' ultimo parametro che serve proprio per specificare in quale direzione si vogliono copiare i dati)
  //la sua sintassi è del tipo:
  //cudaError_t cudaMemcpy(void* dst, const void* src, size_t count, cudaMemcpyKind kind);
  //dove ho:
  //dst → puntatore alla destinazione (ricorda che d_A.elements è un array/puntatore di elementi
  //e quindi posso passarlo alla funzione cudaMemcpy)
  //src → puntatore alla sorgente
  //count → numero di byte da copiare
  //kind → tipo di copia (da dove a dove, ad esempio cudaMemcpyDeviceToHost copia dalla GPU alla CPU)

  err = cudaMemcpy(d_A.elements, A.elements, size, cudaMemcpyHostToDevice);






//anche qui solita logica di prima per cudaGetErrorString(err)
  printf("Copy A to device: %s\n",cudaGetErrorString(err));



  //stesso procedimento di copia da CPU a GPU anche per la matrice B
  Matrix d_B;
  d_B.width = B.width;
  d_B.height = B.height;
  size = B.width * B.height * sizeof(float);
  err = cudaMalloc(&d_B.elements, size);
  printf("CUDA malloc B: %s\n",cudaGetErrorString(err));
  err = cudaMemcpy(d_B.elements, B.elements, size, cudaMemcpyHostToDevice);
  printf("Copy B to device: %s\n",cudaGetErrorString(err));



  // Allocate C in device memory 
  //ora alloco memoria nella GPU per la matrice C che verrà calcolato dal Kernel nella GPU
  Matrix d_C;
  d_C.width = C.width;
  d_C.height = C.height;
  size = C.width * C.height * sizeof(float);
  err = cudaMalloc(&d_C.elements, size);
  printf("CUDA malloc C: %s\n",cudaGetErrorString(err));


 float time;

  cudaEvent_t start,stop;
  //cudaEvent_t è un tipo speciale di CUDA che rappresenta un evento temporale sulla GPU
  //è usato per misurare il tempo di esecuzione di kernel o operazioni sulla GPU

  cudaEventCreate(&start)
  cudaEventCreate(&stop)

 //cudaEventCreate inizializza l’evento che avverrà sulla GPU (nel nostro caso l' esecuzione del Lernel)
 //cioè con queste 2 righe di codice sottostanti sto preparando le variabili start e stop a partire 

 //cudaEventCreate(&start) serve per passare l' indirizzo di start alla funzione cudaEventCreate la quale
 //preparerà la variabile a registrare un timestamp sulla GPU
 

 //start time  
 //chiamata dell' evento start, inizia il tempo cioè salva il timestamp sulla GPU
  cudaEventRecord(start);



//3° compito della CPU: chiamare l' esecuzione del kernel


  // Invoke kernel
  //qui chiamiamo l'esecuzione del kernel con delle specifiche di esecuzione precise
  //in particolare scegliamo il numero di blocchi e di griglie in modo da avere un thread per ogni
  //elemento della matrice C cioè per ogni elemento da calcolare
  // 1 thread = calcolo di 1 elemento di matrice C

  dim3 dimBlock(BLOCK_SIZE, BLOCK_SIZE);
  //ricordo BLOCK_SIZE = 16
  //definisco qui un blocco bidimensionale
  //in CUDA non esiste un tipo dim2, perciò uso dim3 che è un tipo generico 3D con campi x, y, z 
  //anceh per generare un blocco 2D (si genera semplicemente ignorando la componente z)




  //anche per la griglia scelgo di lavorare con 2D
 //dimBlock.x è la grandezza del blocco nella dimensione x 
 //all' interno di questa griglia ogni thread avrà le sue cooordinate globali 
 //in particolare essendo una griglia 2dim ogni thread ha 2 coordinate globali (solita formula)
 //int coordinata_y = blockIdx.y * blockDim.y + threadIdx.y (coordinata Y scorre sulle righe della griglia/matrice)
//int coordinata_x = blockIdx.x * blockDim.x + threadIdx.x (coordinata X scorre sulle colonne della griglia/matrice)


//la quantità B.width / dimBlock.x indica quanti blocchi servono lungo la dimensione x
//tuttavia questo può non essere un numero intero e quindi aggiungo (dimBlock.x - 1)/dimBlock.x
//per arrotondare per eccesso ((dimBlock.x - 1)/dimBlock.x) è un numero minore in (0,1)
//Esempio: B.width = 33 ; BLOCK_SIZE = 16
//allora ho (33 + 16 - 1) / 16 = 48 / 16 = 3 blocchi su una dimensione

  dim3 dimGrid((B.width + dimBlock.x - 1) / dimBlock.x,

	       (A.height + dimBlock.y - 1) / dimBlock.y);

//nota che ho in una dimensione della griglia B.width, mentre nell' altra A.height
//questo è coerente con il fatto che nel prodotto tra matrici A*B = C ho
//che Larghezza A deve essere uguale a Altezza B per poter moltiplicare da cui
//(Altezza A, Larghezza A) * (Altezza B, Larghezza B) = (Altezza A, Larghezza B) 
//cioè Altezza C =  Altezza A, Larghezza C = Larghezza B



  

  //esecuzione del kernel con le specifiche soprariportate e con gli argomenti scelti
  // sotto c'è il kernel MatMulKernel
  MatMulKernel<<<dimGrid, dimBlock>>>(d_A, d_B, d_C);

  err = cudaThreadSynchronize();
  //cudaThreadSynchronize() serve per aspettare che tutti i thread abbiano finito
  //di lavorare prima di procedere (ha senso perchè prima di fermare il tempo di esecuzione con cudaEventRecord(stop)
  //voglio che tutti i thread hanno finito)
  //la funzione ritorna cudaSuccess	se  kernel completato senza errori
  //oppure ritorna cudaErrorLaunchFailure	se il kernel ha fallito durante l’esecuzione


//stop time
  cudaEventRecord(stop); //salva il timestamp sulla GPU
  cudaEventSynchronize(stop); //serve a dire alla CPU di aspettare che la GPU abbia registrato stop prima di proseguire
  //senza cudaEventSynchronize, il calcolo del tempo(che viene eseguito sulla CPU)
  //potrebbe essere errato perché stop potrebbe non essere ancora stato registrato

  cudaEventElapsedTime(&time, start, stop); //calcola nella CPU la differenza in millisecondi tra start, stop e la inserisce in time
  //di cui fornisco l' indirizzo di memoria. Notiamo che time definita sopra è una variabile che vive nella CPU
  

 //mi faccio stampare l' esito dell' esecuzione del kernel leggendo la variabile err di tipo cudaError_t
  printf("Run kernel: %s\n", cudaGetErrorString(err));

 //print time
  printf("Time: %3.5f ms\n",time);
    

//4° compito della CPU: copio i risultati (calcolati dalla GPU) sulla CPU


  // Read C from device memory
  err = cudaMemcpy(C.elements, d_C.elements, size, cudaMemcpyDeviceToHost);
  //con questa riga copio i valori di C dalla GPU (Device) all' Host (CPU)
  //per questo l' ultimo argomento della funzione è cudaMemcpyDeviceToHost

  //mi faccio stampare l' esito dell' operazione di copia
  printf("Copy C off of device: %s\n",cudaGetErrorString(err));



  // Free device memory 
  //è buona norma liberare la memoria allocata precedentemente
  cudaFree(d_A.elements);
  cudaFree(d_B.elements);
  // cudaFree(d_C.elements);
}


//MatMul -> gestita dall' host(CPU)
//MatMulKernel -> gestita dal device(GPU)


// Matrix multiplication kernel called by MatMul()
//questo è il kernel da far eseguire alla GPU contiene azioni da farle eseguire in parallelo
//esso è chiamato nella funzione MatMul la quale viene gestita dalla CPU

__global__ void MatMulKernel(Matrix A, Matrix B, Matrix C) {


  // Each thread computes one element of C, by accumulating results into Cvalue

  //quindi faccio la moltiplicazioni tra matrici
  //facendo processare ad un singolo thread un singolo elemento della matrice C
  //il risultato dell' operazione del singolo thread viene salvato nella variabile Cvalue
  
  float Cvalue = 0.0;

  int row = blockIdx.y * blockDim.y + threadIdx.y;
  int col = blockIdx.x * blockDim.x + threadIdx.x;

  if(row > A.height || col > B.width) return; // or si indica con ||
 //se almeno una delle due è vera, il thread esce subito con return
 //infatti la coordinata riga del thread non può essere più grande della A.height 
 //vorrebbe dire che sono fuori dalla matrice che voglio calcolare
  //quindi questa riga serve per evitare che thread “extra” calcolino fuori dai limiti della matrice

  for (int e = 0; e < A.width; ++e)

  //parte il prodotto riga per colonna per calcolare l' elemento c
  //la varibile e scorre tutte le colonne di A: C[row][col]= somma su e {​A[row][e] * B[e][col] }
  //cioè "e" viene sommato su tutte le colonne di A, righe di B

  //ricordiamo che noi abbiamo accesso agli elementi delle matrici A, B soltanto sotto forma di vettore
  //float* A.elements, B.elements, da cui la formula di conversione sottostante:
  //A[row][e] = A.elements[row *  A.width + e]

    Cvalue += (A.elements[row * A.width + e]) * (B.elements[e * B.width + col]);

    //il valore calcolato: Cvalue viene salvato in posizione row * C.width + col del vettore C.elements 
    C.elements[row * C.width + col] = Cvalue;



}











// Usage: multNoShare a1 a2 b2
int main(int argc, char* argv[]){




  //char* argv[] è un array parole
  //char parola[] è un array di caratteri cioè una parola
  // in C scrivere char* argv[] = char** argv
  //argv[i] è la parola i-esima



  Matrix A, B, C; //con Matrix variabile speciale "struttura" definite
  //nell' header importato, attualmente vivono solo nella CPU


  int a1, a2, b1, b2;

  //a1, a2 dimensioni della matrice A


  // Read some values from the commandline
  //atoi serve per convertire una stringa in un numero intero

  a1 = atoi(argv[1]); /* Height of A */

  //argv[1] è la seconda stringa che viene convertita in un intero
  //dalla funzione atoi
  //per esempio inserendo "502" atoi lo converte nella variabile di tipo int a1 = 502


  //stessa cosa per gli altri uso atoi

  a2 = atoi(argv[2]); /* Width  of A */

  b1 = a2;           /* Height of B */ 
  //necessariamente una dimensione deve coincidere
  //per poter fare il prodotto riga colonna tra 2 matrici quindi b1 = a2

  b2 = atoi(argv[3]); /* Width  of B */



  //una volta che ho inizializzato i valori di a1, a2, b1, b2 
  //avendo convertito l' array di stringhe argv (che conteneva le dimensioni di tutte e 2 le matrici)
  //posso inizializzare anche gli attributi di A e B

  A.height = a1; //attributo altezza della matrice A che vive nella CPU
  A.width = a2;

  //alloco memmoria 
  A.elements = (float*)malloc(A.width * A.height * sizeof(float));


  B.height = b1;
  B.width = b2;
  B.elements = (float*)malloc(B.width * B.height * sizeof(float));


  C.height = A.height;
  C.width = B.width;
  C.elements = (float*)malloc(C.width * C.height * sizeof(float));


//creo una matrice casuale A con 2 cicli for concatenati, uno che scorre sulle righe, 
//l' altro sulle colonne j
  for(int i = 0; i < A.height; i++)
    for(int j = 0; j < A.width; j++)
    //in verità non riempio una marice ma un array contenenti tutti gli elementi della matrice
    // e quindi mi serve la formula di "proiezione 1dim"

      A.elements[i*A.width + j] = (float)(random() % 2);

      //(float)(random() % 2) crea un numero casuale di tipo float in questo modo


 //idem per B 

  for(int i = 0; i < B.height; i++)
    for(int j = 0; j < B.width; j++)
      B.elements[i*B.width + j] = (float)(random() % 3);





  //nel main chiamo la funzione MatMul dove moltiplico le 2 matrici
  //random A, B e calcolo la matrice C, ricordiamo che MatMul è la funzione eseguita dall' host (CPU)
  //che dopo aver allocato memoria e copiato i dati da CPU a GPU, ad un certo punto, 
  //chiamerà il kernel per far eseguire la moltiplicazione tra matrici
  //dalla GPU, in cui il kernel verrà eseguito usando 1 thread per ogni elemento da calcolare
  //la CPU nella funzione MatMul si occuperà di ricopiare i risultati da GPU a CPU
  MatMul(A, B, C);





  //la funzione MatMul non restiuisce nulla poichè di tipo void,
  //non viene stampato nulla, se voglio visualizzare qualcosa c' è il codice qui sotto...
  
  /*
  // Print up to a 10x10 portion of the three matrices
  for(int i = 0; i < min(10, A.height); i++){
    for(int j = 0; j < min(10, A.width); j++)
      printf("%f ", A.elements[i*A.width + j]);
    printf("\n");
  }
  printf("\n");
  for(int i = 0; i < min(10, B.height); i++){
    for(int j = 0; j < min(10, B.width); j++)
      printf("%f ", B.elements[i*B.width + j]);
    printf("\n");
  }
  printf("\n");
  for(int i = 0; i < min(10, C.height); i++){
    for(int j = 0; j < min(10, C.width); j++)
      printf("%f ", C.elements[i*C.width + j]);
    printf("\n");
  }
  printf("\n");
  */

}
