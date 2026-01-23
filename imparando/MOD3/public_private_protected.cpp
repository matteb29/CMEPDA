#include <iostream>
#include <cmath>
using namespace std;

class Particle{

    //definisco un attributo privato che non è accessibile alle particelle figlie
    private:

        float higgs_potential = 240.0;

    public:

        //metodi pubblici e virtuali
        virtual void rilascio(){

            double energia_rilasciata = 100.0;
            cout<<"la particella ha rilasciato"<<energia_rilasciata<<"GeV";

        }

    //qui metto qualcosa che non è modificabile dall' 
    //esterno ma che è accessibile alle classi figlie, tipo la massa
    protected:
        float mass = 140;

        //facciamo un metodo protected con una variabile privata per farci dare errore
        void return_higgs_field(){
            cout<<higgs_potential;

        }

};

class Elettrone : public Particle{

    public:

        void rilascio() override{

            double energia_rilasciata = 30.0; 
            cout<<"energia rilasciata"<<energia_rilasciata<<"MeV";
        }


    protected:
        double massa = 0.511;


};


int main(){

    Elettrone e;
    e.rilascio();

    //cout<<"massa dell' elettrone"<<Elettrone.massa;
    //questa sopra non funziona visto massa è un attributo protected
    //cioè pubblico per le figlie ma privato per il main

    //vediamo che se provo ad accedere all' higgs potential dà errore (declared protected here)
    //e.return_higgs_field();


return 0;
}