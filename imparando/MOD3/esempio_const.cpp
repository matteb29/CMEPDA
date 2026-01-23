#include <iostream>
using namespace std;

class Automobile{

    public:

        int ruote_macchina = 4;

        void smonta_ruote() const {

            cout<<"smonto ruote"<<endl;
            //ruote_macchina = 0;
            cout<<ruote_macchina<<endl;

            //posso modificare delle variabile interne 
            int numero_freni = 5;
            numero_freni = 7;

            cout<<"i freni te li lascio, sono: "<<numero_freni<<endl;

        }



};


int main(){

    Automobile alpha_gt;
    alpha_gt.smonta_ruote();



    return 0;
}


