#include<iostream>
#include<vector>
using namespace std;


int main(){

    std::vector<int> vettore = {10, 11, 12};

    std::vector<int>::iterator iteratore;

    iteratore = vettore.begin();

    cout<<*iteratore<<endl;
    iteratore++;

    cout<<*iteratore<<endl;






    return 0;
}