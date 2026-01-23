#include <iostream>
using namespace std;

//questa va compilata con -std=c++14





template <typename T1, typename T2>
auto somma(T1 a, T2 b){
    return a + b;
}



int main(){

    auto risultato = somma(5, 5.7);
    cout<<risultato<<endl;

    return 0;
}