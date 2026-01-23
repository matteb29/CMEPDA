#include <iostream>
using namespace std;


int taglia_numero(double x){
    return x;
};






class Singleton{

    private:
        Singleton(){

            //costruttore privato 


        }

    public:

        //definiamo il metodo get come statico perchè
        //dovrà essere chiamato a prescindere dall' istanzializzazione
        static Singleton& get(){

            //metto static anche alla reference perchè una funzione static
            //può lavorare solo con variabili static
            static Singleton reference_istanza_singleton;

            //l' istanza te la restituisce sotto forma di reference
            return reference_istanza_singleton;
        }

      

};


int main(){

    //qui mi resituisce gli stessi indirizzi di memoria perchè sia reference1 che reference 2 fanno
    //riferimento al solito oggetto
    Singleton& reference1 = Singleton::get();

    Singleton& reference2 = Singleton::get();


    cout<<&reference1<<endl<<&reference2<<endl;


    //esempio per far vedere che comanda sempre il tipo restituito
    cout<<taglia_numero(9.876)<<endl;







    return 0;
}