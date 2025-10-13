
//con questo programma vogliamo fare chiarezza sull' utilizzo di array 
// e puntatori in c++, esplicando analogie e differenze
// in C/C++ puoi usare i puntatori per definire vettori non inizializzati 
//cioè blocchi di memoria che decidi tu di allocare in seguito


#include <iostream>
using namespace std;

int main(){

    int x =  42;
    int *p = &x;
    cout << p << endl;
    cout << &x << endl;
    cout << *p << endl;



    int array[] = {10, 20, 30};
    int * puntatore_array = array;
    cout << puntatore_array << endl;
    cout << &puntatore_array <<endl;    
    cout << array[1] << endl;
    cout << puntatore_array[1]<< endl;
    cout << "Indirizzo del primo numero: " << static_cast<void*>(puntatore_array) << endl;


    int* puntatore_primo_elemento = &array[1];
    cout << puntatore_primo_elemento<<endl;




    char* parola = "ciao";
    cout << parola <<endl;

    char parola2[] = "ciao";
    char* puntatore_parola = parola2; 
    cout << "Indirizzo del primo carattere: " << static_cast<void*>(puntatore_parola) << endl;
    cout << puntatore_parola << endl;

    char bestemmia[] = "dio bastardo";
    char* blasfemia = "dio bastardo";

    for (int i = 0; i < 3; i++){
        cout << bestemmia[i] << endl;
    }

    char * bestemmie[] = {"dio porcone", "dio cane", "dio infame"};
    cout << bestemmie[1] << endl;

    return 0;


}
