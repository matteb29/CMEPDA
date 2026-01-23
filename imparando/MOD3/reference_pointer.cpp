#include <iostream>
using namespace std;

int main(){

    int a = 100;
    int b = 200;

    //assegniamo una reference alla variabile a, ricorda che non posso non inizializzare una ref
    //sintassi TIPO + & + NOME_REF = VARIABILE_ESISTENTE;

    int& ref = a;
    cout<<"il valore della variabile a è accessibile tramite ref ora: "<<ref<<endl<<endl;
    cout<<"l' indirizzo di memoria della variabile a è accessibile tramite &ref ora: "<<&ref<<endl<<endl;

    //proviamo a riassegnare una ref
    ref = b;

    cout<<"anche se riassegniamo la ref il suo indirizzo non cambia: "<<&ref<<endl<<endl;
    cout<<"tuttavia cambia il suo valore: "<<ref<<endl<<endl;

    //ora proviamo con i puntatori

    int* puntatore1 = &b;
    int* puntatore2 = nullptr; //se non lo inizializzo punta ad un indirizzo casuale


    cout<<"l' indirizzo della variabile b è accessibile tramite puntatore: "<<puntatore1<<endl<<endl;
    cout<<"il valore della variabile b è anch' esso accessibile tramite puntatore: "<<*puntatore1<<endl<<endl;

    //mostriamo che la riassegnazione funziona con i puntatori
    puntatore1 =  &a;

    cout<<"l' indirizzo di memoria a cui punta puntatore1 è ora cambiato dopo la riassegnazione: "<<puntatore1<<endl<<endl;



return 0;
}