#include <iostream>
using namespace std;


class Automobile{

    public: 

        int numero_ruote;
        double conta_km;

        Automobile(int numero_ruote, double conta_km){

            this->numero_ruote = numero_ruote;
            this->conta_km = conta_km;


        }

        void accendi_motore(){
            cout<<"brum"<<endl;
            cout<<"stiamo usando un oggetto che vive nel seguente spazio di memoria: "<<endl<<this<<endl;

        }



};


int main(){

    Automobile alpha_gt(4, 1000.0);

    //nota che gli attributi sono definiti nel solito indirizzo di memoria dell' oggetto
    cout<<&alpha_gt.numero_ruote<<endl;
    cout<<&alpha_gt.conta_km<<endl;

    cout<<&alpha_gt<<endl;

    alpha_gt.accendi_motore();

    

return 0;
}