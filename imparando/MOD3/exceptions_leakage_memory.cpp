#include <iostream>
using namespace std;



void funzione_leakage_memory(){

    //allochiamo memoria per 100 interi
    //nota che la variabile puntatore vive nella stack
    //mentre avendo scritto new l' array di 100 interi vive nella heap
    int* puntatore = new int [100];
    
    //facciamo vedere che questa memoria è stata allocata stampando la prima cella occcupata
    cout<<endl<<endl<<"memoria allocata: "<< puntatore<<endl<<endl;

    //creiamo un codice con possibilità errori
    int a = 10;
    int b;
    cout<<"Inserisci un numero : ";
    cin>>b;

    if (b == 0){

        //qui viene lanciato un errore che interrompe il normale flusso di esecuzione del codice
        //la funzione si chiude, quindi non viene più eseguito il codice sottostante

        //delete[] puntatore;
        throw std::runtime_error("");
        

    }else{

        double divisione = a / b;
        cout<<divisione<<endl<<endl;
    }

    //qui deallochiamo la memoria
    delete[] puntatore;
}







int main(){

//qui lanciamo il (try, catch) della funzione che causa leakage memory
try{
    funzione_leakage_memory();
}

//se arriviamo al catch abbiamo ottenuto il leakage memory (non si vedranno messaggi al riguardo)
catch (const std::exception& e){
    cout<<"catturata eccezione nel main"<<endl<<e.what()<<endl<<endl;
    //e.what restituisce il messaggio di errore che abbiamo impostato noi "Errore!!!"
}


return 0;
}