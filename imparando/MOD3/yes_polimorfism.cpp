#include <iostream>
using namespace std;

class Animale{

    public:

        virtual void fai_verso(){
            cout<<"dio cane"<<endl;
        }

        void rispondi_domanda(){
            fai_domanda();
            cout<<"si"<<endl;
        }

    private: //facciamo vedere che i metodi privati posso chiamarli dentro altri metodi della stessa classe
    //in cui li ho definiti

        void fai_domanda(){
            cout<<"sei vivo?"<<endl;
        }

        int numero_zampe;

       


};

class Cane : public Animale{

    public:

        void fai_verso(){
            cout<<"bau"<<endl;
        }

    private:
        void bestemmia(){
            cout<<"viva la ricerca libera e indip"<<endl;
        }


};

void chiama_fai_verso(Animale* generico_animale ){

    generico_animale -> fai_verso();



    return ;
}



int main(){

    Cane pepe;
    Animale persona;

    pepe.fai_verso();
    persona.fai_verso();

    cout<<endl<<endl;

    chiama_fai_verso(&pepe);


    persona.rispondi_domanda();

   // persona.fai_domanda();





    return 0;
}