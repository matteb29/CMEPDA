#include <iostream>
using namespace std;

//in c++ le funzioni non possono essere definite dentro il main, solo le
//lambda function possono essere definite dentro il main
int calcola_numero(int num_a, int num_b){
       return num_a + num_b;
    };

void definisce_lambda_function(int a){

    auto lambda_function = [a](){
        cout<<a<<endl;
    };

    lambda_function();

    return;
};


int main(){

    //-------------------
    //di seguito quello che avrei dovuto fare nel main se 
    //volessi fare due somme senza definire una funzione
    int c = 5;

    int num1 = 3;
    int num2 = 4;
    int somma1 = num1 + num2;

    cout<<somma1<<endl;

    int num3 = 5;
    int somma2 = somma1 + num3;

    //-------------------------

    { //scope di definizione della lambda function

    int numero_nascosto = 3;
    //lambda function
    auto somma = [c](int a, int b){

        //nota che non puoi definire una funzione nel main
        //nemmeno dentro una lambda

       // void stampa(int f){
         //   cout<<f<<endl;
           // return;
        //}

        //stampa(5);
        //stampa(6);
        return c+a+b;
    };

    //chiamo la lambda function 2 volte
    cout<<somma(3,6)<<endl;
    cout<<somma(2,9)<<endl;

    }


    //la lambda function non esiste fuori dallo scope in cui la definisco
    //cout<<somma(5,6)<<endl;

    //ovviamente non vedo nemmeno variabili definite dentro lo scope
    //cout<<numero_nascosto<<endl;
    cout<<calcola_numero(4,5)<<endl;


    definisce_lambda_function(4);



    return 0;
}