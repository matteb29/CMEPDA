#include <iostream>
using namespace std;

//qui implemento tutto a mano
class Animale_distruttore{

    private:
        int* età;


    public:

        Animale_distruttore(int età){
            cout<<"questo è il costruttore"<<endl;
            this->età = new int(età);
            cout<<"salvo la variabile età dell' animale nella cella di memoria"<<this<<endl<<endl<<età<<endl;;

        }




        ~Animale_distruttore(){

            cout<<endl<<"questo è il distruttore"<<endl;
            cout<<"in automatico lui libera questo indirizzo di memoria: "<<this<<endl;
            cout<<"ma noi vorremmo liberare questa: "<<età<<endl;
            

            //dealloco memoria che altrimenti non sarebbe deallocata
            delete(età);
            cout<<"ho liberato la memoria della variabile età";

        }

        //costruttore di copia per creare una nuova copia dell' animale che vive in spazi di
        //memoria proprio

        Animale_distruttore(const Animale_distruttore& clone_animale){
            cout<<endl<<"ora si è attivato il costruttore di copia poichè ho creato una copia dell' istanza";
            età = new int(*clone_animale.età);
            cout<<età;
        }

        //vecchio animale = nuovo animale;
        //metodo speciale 
        Animale_distruttore& operator=(const Animale_distruttore& nuovo_animale){

            cout<<"all' inizio ho età salvata in questa cella di memoria:"<<età<<endl<<*età<<endl;
            delete(età);
            età = new int(*nuovo_animale.età);
            cout<<"ora età è in questa cella di memoria"<<età<<endl<<*età<<endl;

            
            return *this;            
        }






};


class Animale{


        

    public:
        int* età;
        Animale(int anni){
            cout<<endl<<"questo è il costruttore, qui non ho distruttore"<<endl<<endl;
            età = new int(anni);

        }

    //qui il distruttore è implicito

    //qui il costruttore di copia è implecito

};


int main(){

   
   {

    Animale cane(3);
    Animale clone_cane = cane;
   
    cout<<"ora tutto esplicitato"<<endl<<endl;
    Animale_distruttore cane_distruttore(10);
    //qui si applica il costruttore di copia
    Animale_distruttore clone_cane_distruttore = cane_distruttore;


    cout<<endl<<endl<<&clone_cane_distruttore<<endl<<endl<<&cane_distruttore;
    cout<<endl<<endl<<&clone_cane<<endl<<endl<<&cane<<endl<<endl<<endl;


    cout<<clone_cane.età<<endl<<cane.età;
   }


   {

    cout<<endl<<endl<<endl<<"operatore di assegnazione di copia"<<endl;
    Animale_distruttore cloneA(6);
    Animale_distruttore cloneB(7);

    Animale clone1(3);
    Animale clone2(4);

    clone1 = clone2;

    //senza esplicitare il operator= entrambi vivono nel solito indirizzo di memoria
    cout<<"dio cane!"<<endl<<*clone1.età<<endl;
    cout<<"dio bastardo!"<<endl<<clone1.età<<endl<<clone2.età<<endl;

    //Animale_distruttore cloneC = cloneA;


    //operatore di assegnazione di copia
    //cloneA continuerà a chiamarsi cloneA, ma avrà l' età di cloneB
    cloneA = cloneB;




   }

   








    return 0;
}