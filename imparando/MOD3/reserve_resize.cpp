#include <iostream>
#include <vector>
using namespace std;

int main(){

    //creiamo un vettore di interi 
    std::vector<int> vettore;

    //vediamo l' indirizzo di memoria (la prima cella)
    cout<<"indirizzo di memoria iniziale in cui è allocato il vettore: "<<&vettore<<endl<<endl;


    //allochiamo dello spazio in memoria per poter scrivere un vettore di 100 interi
    vettore.reserve(100);

    //mostriamo questo spazio in memoria riservato (la 99-esima cella)
    cout<<"lo spazio in memoria riservato al vettore di 100 interi: "<<&vettore[99]<<endl<<endl;

    //vediamo che non esiste ancora l' oggetto vettore:
    //attualmente la size è 0 perchè non ci sono elementi

    //cout<<vettore.at(1)<<endl<<endl;
    //infatti mi dà errore out of range!!
    
    //creiamo l' oggetto vettore nel primo slot di memoria allocata, aggiungendo al vettore il numero 20
    vettore.push_back(20);

    //ci accorgiamo che 100 numeri non ci servono, facciamo il resize a 5
    vettore.resize(5);

    //mostriamo che l' oggetto esiste ed è stato inizializzato a zero, cioè la size è diversa da 0, 
    //lo spazio vuoto è stato riempito con zeri
    cout<<vettore[4];








}