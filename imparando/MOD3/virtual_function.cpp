#include <iostream>
#include <vector> //per poter definire vettori di oggetti
using namespace std;

//creiamo una classe madre
class Madre {

    public:
       
       //definiamo un metodo virtuale
        virtual void chiSono() {
            cout << "sono la madre" << endl;
        }
        //definiamo un metodo statico
        void bestemmia(){
            cout<<"dio cane!"<<endl;
        }

};

//creiamo una classe figlia ereditaria di Madre
class Figlio_maschio : public Madre{

    public:

        //override è un controllo del fatto che chiSono appartenga effettivamente alla madre
        void chiSono() override{
            cout<<"sono il figlio"<<endl;
        } 

        void bestemmia(){
            cout<<"dio porco!"<<endl;
        }

};

class Figlia_femmina : public Madre{

    public:

    void chiSono() override{
        cout<<"sono la figlia"<<endl;
    }

    void bestemmia(){
        cout<<"dio infame!"<<endl;
    }

};

void ciclo_chiSono(){

    //definiamo un vettore di oggetti madre
    vector<Madre*> famiglia;

    //aggiungiamo elementi al vettore famiglia 
    famiglia.push_back(new Madre());
    famiglia.push_back(new Figlia_femmina());
    famiglia.push_back(new Figlio_maschio());

    for(Madre* persona : famiglia){

        persona->chiSono();




    }


return;

};





int main(){

    //creiamo una variabile f di tipo Figlia
    Figlio_maschio f;
    Figlia_femmina g;

    f.chiSono();

    g.chiSono();

    



    //prendiamo l' indirizzo di memoria della f 
    //il suo valore lo salviamo in un puntatore di tipo Madre
    //per puntare ad una variabile di tipo madre ho bisogno di un puntatore di tipo madre

    //in linea di principio potrei usare Figlia*
    //tuttavia se ho più classi ereditarie figlie della solita madre
    //posso raggruppare tutte le classi scrivendo Madre*
    Madre* puntatore_maschio = &f;
    Madre* puntatore_femmina = &g;

    //chiamiamo il metodo chiSono usando un puntatore
    //nella pratica vuol dire andare all' indirizzo di memoria della variabile f e poi applicare il metodo chiSono
    puntatore_maschio -> chiSono();
    puntatore_femmina -> chiSono();



    //mostriamo ora che senza virtual non ho polimorfismo cioè:

    //se chiamo il metodo bestemmia direttamente da f
    f.bestemmia();

    
    //è diverso che chiamarlo da puntatore, infatti quindi restituiscono entrambe
    //le bestemmie della madre, non le loro singole
    puntatore_maschio->bestemmia();
    puntatore_femmina->bestemmia();

    cout<<endl<<endl<<"Inizia il ciclo di chi sono.."<<endl;
    ciclo_chiSono();

return 0;
}