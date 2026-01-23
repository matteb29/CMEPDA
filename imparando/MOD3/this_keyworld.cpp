#include <iostream>


using namespace std;

class Particle{

    //tutto ciò che scrivo prima del public è automaticamente privato
    //immaginiamo una variabile privata che si chiama "energy" in cui salviamo l' enrgia inizializzata
    //al momento dell' istanza
    double energy;
    double mass;
    

    public:

        double impulso;


        //definiamo il costruttore della classe, identico a quando scriviamo __init__ in python
        //il costruttore non ha davanti nulla a Particle, è l' unica funzione che non restituisce nulla, 
        //nemmeno il vuoto, 
        //deve stare sotto public così posso chiamarlo con il main
        Particle(double energy, double particle_mass, double particle_impulso){

            //questa riga di codice è equivalente a chiamare self.energy = energy in python
            //se mi ostino a voler chiamare l' attributo della classe Particle come "energy" (cioè uguale alla variabile privata sopra)
            // devo risolvere l' ambiguità usando il self
            this->energy = energy;

            //qui non c' è bisogno di specificare il this perchè parametro del costruttore e variabile interna
            // si chiamano in due modi diverse
            mass = particle_mass;

            impulso = particle_impulso;

            
               // potrei risolvere l' ambiguità scrivendo:

                //Particle(double e){
                
                  //  energy = e;
                //}
            

        }

        //stampiamo un semplice metodo
        void controlla_Indirizzo(){
            cout<<"Indirizzo dell' istanza"<<this<<endl;
        }

};

int main(){

    Particle p(100, 50, 30);

    cout<<"nel main l' indirizzo di p è dato da &p: "<<&p;

    //facciamo stampare il this del p, poichè il this restituisce un
    //puntatore all' oggetto ciò che vedremo deve coincidere con ciò che stampa la riga di codice sopra
    p.controlla_Indirizzo();


  //questo no perchè massa è privato!  cout<<"massa della particella: "<< p.mass<<endl;

    cout<<"impulso della particella: "<<p.impulso<<endl;






return 0;
}