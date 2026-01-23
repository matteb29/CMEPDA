#include<iostream>
#include<vector>
#include <list>
using namespace std;


int main(){

    std::vector<int> vettore = {10, 11, 12};

    std::vector<int> vettore2 = {20,30,40};

    std::vector<int> vettore_somma;


    std::vector<int>::iterator iteratore;

    iteratore = vettore.begin();

    cout<<*iteratore<<endl;
    iteratore++;

    *iteratore += 1000;

    cout<<*iteratore<<endl<<endl;
   
    for (int i = 0; i<3; i++){
        cout<<vettore[i]<<endl;
        cout<<&vettore[i]<<endl<<endl;
    }


    const std::vector<int>::iterator iteratore_const = vettore.begin();

    cout<<endl<<endl<<*iteratore_const<<endl<<endl;



    //usiamo liste

    list<int> lista = {10,20,30};

    list<int>::iterator iteratore_lista = lista.begin();


    
 







    return 0;
}