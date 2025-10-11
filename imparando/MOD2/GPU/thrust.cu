#include <thrust/host_vector.h>
#include <thrust/device_vector.h>
#include <thrust/transform.h>
#include <thrust/functional.h>   // per placeholders come _1, _2
#include <iostream>



int main(){

int a = 42;
int n = 10;

//qui creo usando thrust due vettori x(n) e y(n) nella CPU
thrust::host_vector<float> x(n);
thrust::host_vector<float> y(n);



//riempio i vettori della cpu

    for (int i = 0; i < n; i++) {
        x[i] = i;
        y[i] = i * 2;
    }



//qua invece creo dei vettori nella GPU usando thrust, inizializzati agli array
// delle cpu x, y
thrust::device_vector<float> d_x = x;
thrust::device_vector<float> d_y = y;


//serve per poter usare i segnaposto e riferirsi ad un elemento
//specifico di un vettore thrust come ad esempio in riga 42 a* _1 indica a* elemento 1 del vettore in GPU
using namespace thrust::placeholders;


//esecuzione del calcolo parallelo su GPU usando thrust (equivalente di un ciclo for sulla GPU)
thrust::transform(d_x.begin(), d_x.end(), d_y.begin(), d_y.begin(), a * _1 + _2);

//.begin() e .end() sono inizio e fine del vettore
//.begin() è un puntatore al primo elemento dell' array
//.end() è un puntatore all' ultimo elemento +1 dell' array

//a * _1 + _2 significa dy​[i]= a * dx​[i]+ dy​[i]
//i placeholder 1_ e 2_ funzionano come 
//_1 → l’elemento corrente del primo vettore (d_x[i])
//_2 → l’elemento corrente del secondo vettore (d_y[i])



//la sintassi thrust::transform è la seguente 
//thrust::transform(first1, last1, first2, result, unary_or_binary_op);
//con : first1, last1 → intervallo del primo input
//first2 → intervallo del secondo input (solo se stai usando l’operazione binaria)
//result → dove salvare il risultato
//unary_or_binary_op → funzione da applicare a ogni elemento in parallelo


//copio i risultati dei calcoli fatti sulla GPU in CPU
x = d_x;

cout<<x;

return 0;

}
