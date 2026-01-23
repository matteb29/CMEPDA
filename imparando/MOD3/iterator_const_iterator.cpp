#include <iostream>
#include <vector>
using namespace std;



int main(){

std::vector<int> vettore = {10, 20, 30};


//definiamo un iteratore e inizializziamo al primo elemento del vettore
std::vector<int>::iterator iteratore = vettore.begin();

//mostriamo che con un iteratore posso assegnare valori a elementi
//e leggere elementi del vettore

*iteratore = 100;
iteratore ++;

//definiamo un const_iterator

std::vector<int>::const_iterator iteratore2 = vettore.begin();

//posso scorrere elementi e printarli

cout<<"primo elemento del vettore: "<<*iteratore2<<endl<<endl;
iteratore2++;

cout<<"secondo elemento del vettore: "<<*iteratore2<<endl<<endl;

//non posso modificare elementi del vettore infatti questo mi crea errore
//*iteratore2 = 200;


//vediamo invece un const iterator

//inizializziamo al primo elemento del vettore
const vector<int>::iterator constant_iterator = vettore.begin();

//vediamo che possiamo stampare
cout<<"stampiamo con il constant iterator: "<<*constant_iterator<<endl;
//modificarlo
*constant_iterator = 100;

//ma non possiamo muoverci di lì
//questo dà errore:
//constant_iterator ++;








return 0;
}