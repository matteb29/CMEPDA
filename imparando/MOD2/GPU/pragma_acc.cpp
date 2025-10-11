


void saxpy_acc(int n, float a, float * x, float * y) {

//questo uso di #pragma rappresenta una direttiva cioè
//indicazione da dare alla macchina quando compila il codice
#pragma acc kernels
//in particolare #pragma acc kernels è una direttiva di OpenACC 
//che dice al compilatore che il blocco di codice immediatamente dopo dovrà essere eseguito in parallelo sulla GPU 
//oppure sulla CPU (se non ho a dispozione una CPU)



for (int i = 0; i < n; i++) {
y[i] = a * x[i] + y[i];
}

//OpenACC esegue il ciclo in parallelo
//eseguendo y[i] = 42*x[i] + y[i] per tutti gli elementi dei vettori simultaneamente
//in particolare gestisce automaticamente la copia dei dati dalla CPU alla GPU e viceversa,
//mentre prima con la libreria thrust dove farlo manualmente

}

int main(){
int a = 42;
int n = 10;
float x[n], y[n];
// fill x, y


saxpy_acc(n, a, x, y);

return 0;
}




