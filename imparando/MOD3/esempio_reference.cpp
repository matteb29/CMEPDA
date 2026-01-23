#include <iostream>
using namespace std;


int somma_con_puntatori(int* puntatore1, int* puntatore2){
    return *puntatore1 + *puntatore2;
};




int somma_con_reference(int& reference1, int& reference2){
    return reference1 + reference2;
};




int somma_standard(int a, int b){
    return a + b;
};





int main(){

    int a;

    cout<<&a<<endl;

    a = 10;

    //gestiamo gli indirizzi di memoria

    int* puntatore;
    puntatore = &a;

    int* puntatore_vuoto = nullptr;

    //int& reference_vuoto = nullptr;



    cout<<puntatore<<endl;
    cout<<*puntatore<<endl;

    int& reference = a;
    cout<<reference<<endl;
    cout<<&reference<<endl<<endl;

    //non mi serve più "a"
    int b;
    b = 25;
    puntatore = &b;

    cout<<puntatore<<endl;

    reference = b;



    cout<<reference<<endl;
    cout<<&reference<<endl<<endl;



    //modificando il valore di reference ho anche cambiato il valore di "a"
    cout<<a<<endl<<endl;

    int c = 1000;
    int& reference2 = c;
    

    cout<<somma_con_puntatori(&reference, &reference2)<<endl;
    cout<<somma_con_reference(reference, reference2);

    //cout<<somma_con_reference(&b, &c);

    int d = 7;
   // int& reference3 = &d;


    















    return 0;
}