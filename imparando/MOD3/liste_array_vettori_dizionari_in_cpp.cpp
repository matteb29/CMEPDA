#include <iostream>
#include <vector>
#include <unordered_map>
#include <array>
#include <string>

using namespace std;


//stampare le cose è molto più difficile in c++, bisogna usare dei cicli for

    //fai una copia del vettore che gli passi alla funzione e lo stampi
    //se non voglio copie creo const vector<int>& vettore
    void stampa_vettore(vector<int> vettore){

        for (int n: vettore){
            cout<<n<<endl;
        }

        cout<<endl<<endl;
        return;

    }

    void stampa_dizionario(unordered_map<string, int> dizionario ){

        //un dizionario non ha interi ma coppie chiave valore quindi uso la parola "auto" per far capire
        //al compilatore che lavoro su una coppia
        for (auto elemento_dizionario: dizionario){
            cout<<"persona: "<<elemento_dizionario.first<<endl; //stampo chiave
            cout<<"età: "<<elemento_dizionario.second<<endl; //stampo valore
        }
    }











int main(){

    //vediamo che una lista python si fa con vector
    vector<int> mia_lista = {10,20,30};

    //e l' equivalente python di append: push_back
    mia_lista.push_back(40);


    //vediamo che un dizionarion python si fa con unordered_map
    unordered_map<string, int> mio_dizionario;
    mio_dizionario["Giulio"] = 25;
    mio_dizionario["Fabio"] = 30;

    //cout<<"Il mio dizionario in C++ è: " << mio_dizionario;

    //vediamo che un array python si fa con array se di lunghezza fissa

    array<int, 3> array1 = {1,2,3};
    array<int, 3> array2 = {3,4,5};


    //usiamo la funzione per stampare

    cout<<"stampo vettore: "<<endl;
    stampa_vettore(mia_lista);
    cout<<endl<<endl<<"stampo dizionario: "<<endl;
    stampa_dizionario(mio_dizionario);





    return 0;
}