#include <iostream>
#include <string>

using namespace std;

class Particle{

    public:
        virtual void costruttore(){
            cout<<"ho creato una particella " <<endl;
        }
        virtual void distruttore(){
            cout<<"ho distrutto una particella"<<endl;
        }

        //ora creiamo un metodo const che non mi farà cambiare gli attributi
        void stampa_stato_particella() const{
            cout<<"stato"<<name;
        }

        //ora creiamo un metodo non const che mi farà cambiare gli attributi
        void set_new_energy(int new_energy ){

            //nota che anche se la variabile energy è privata posso modificarla dentro la classe
            energy = new_energy;
            cout<<"energia aggiorata"<<energy;
        }
    
    private:
        int energy;
        string name;

};


//creiamo una funzione con passaggio per riferimento

void test_function_reference(const Particle* p){

    //qui vediamo che se chiamo la funzione set_new:

    p->stampa_stato_particella;
}