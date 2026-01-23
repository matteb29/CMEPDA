#include <iostream>
#include <vector>

using namespace std;


int main(){

    std::vector<int> vettore = {10,11,12,13,14};

    //aggiungo un elemento al vettore
    //in automatico si fa un resize più abbondante
    vettore.push_back(130);

    vettore.push_back(140);

    vettore.reserve(100);

    cout<<vettore[95]<<endl;

    //aggiungo degli 0 nei posti vuoti
    //vettore.resize(10);

    cout<<vettore.size()<<endl;

    cout<<vettore.capacity()<<endl<<endl;

    for (int i = 0; i<6; i++){

        cout<<vettore[i]<<endl;

    }

    return 0;
}