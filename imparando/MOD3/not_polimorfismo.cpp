#include <iostream>
using namespace std;

class Animale{

    public:

        void fai_verso(){
            cout<<"dio cane"<<endl;
        }


};

class Cane : public Animale{

    public:

        void fai_verso(){
            cout<<"bau"<<endl;
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




    return 0;
}