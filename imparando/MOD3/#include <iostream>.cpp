#include <iostream>
using namespace std;

//creiamo una classe madre
class Madre {

    public:
       
       //definiamo un metodo virtuale
        virtual void chiSono() {
            cout << "sono la madre" << endl;
        }

};

//creiamo una classe figlia ereditaria di Madre
class Figlia : public Madre{

    public:

        //override è un controllo del fatto che chiSono appartenga effettivamente alla madre
        void chiSono() override{
            cout<<"sono la figlia"<<endl;
        } 
};


int main(){

    //creiamo una variabile f di tipo Figlia
    Figlia f;

    f.chiSono();

    //prendiamo l' indirizzo di memoria della f 
    //il suo valore lo salviamo in un puntatore di tipo Madre
    //per puntare ad una variabile di tipo madre ho bisogno di un puntatore di tipo madre
    Madre* puntatore = &f;

    //chiamiamo il metodo chiSono usando un puntatore
    //nella pratica vuol dire andare all' indirizzo di memoria della variabile f e poi applicare il metodo chiSono
    puntatore -> chiSono();


s
return 0;
}