#include <iostream>
#include <unistd.h> //libreria per il fork()
#include <sys/wait.h> //libreria per il wait()

using namespace std;


//definiamo una classe SINGLETON
//sua peculiarità è il metodo per creare l' istanza

class logger{

    private:
        int valore; //valore segreto 

        //NOTA CHE IL COSTRUTTORE è PRIVATO QUINDI
        //NON SI PUò CHIAMARE DA FUORI
        //facciamo costruttore privato
        logger(){
            valore = 123;
        }

    public: //facciamo il creatore di istanza pubblico cosi posso creare istanze nel main

        //nota che questo è UN METODO STATIC che ci permette di chiamare il metodo senza averne una istanza
        //questo perchè il metodo static non appartiene ad un oggetto ma è specifico della CLASSE
        //lo possiamo chiamare dal nulla usando il solo nome della classe logger::nome_metodo_statico


        //SINTASSI:
        //static: vuol dire che sto creando un metodo della classe, quindi non servirà creare un oggetto per invocarlo
        // logger& significa che questo metodo deve restituirmi un puntatore ad una variabile logger, cioè l' indirizzo di memoria
        //di una variabile logger
        static logger& getInstance(){
            
            //creiamo la variabile statica "instance" che rimane in memoria per tutto il programma,
            //se non fosse statica ogni volta che chiamo getInstance starei creando una nuova variabile 

            //static: significa che la variabile è statica quindi sarà presente per tutto il programma,
            //ogni volta che chiamo getInstnce chiamo sempre la solita variabile statica, non ne stiamo creando una nuova
            //ad ogni chiamata (come invece accadrebbe con una normale funzione)

            //logger: significa che la variabile è di tipo logger, giusto perchè 
            //stiamo  creando una istanza della classe
            static logger instance; 
            
            return instance;

        }

        //un esempio in cui this risolve l' ambiguità tra parametro del metodo setValore e variabile interna della classe
        //nota che questo metodo pubblico ci permette di accedere alla variabile privata "valore"
        //possibile perchè privato vuol dire non accessibile dall' esterno, ma si dal solito blocco 
        //così controlliamo noi come è permesso cambiare "valore"
        void setValore(int valore){

            if (valore > 0){
                this->valore = valore;
            }else{
                cout<<"il valore non può essere negativo";
            }

        }

        //poichè valore è una variabile privata dobbiamo farcela stampare con un metodo
        int stampa_valore(){

            //per valore qui si intende l' attributo della classe
            return valore;
        }

        //NOTA che l' unico metodo statico è getInstance, gli altri sono "normali"
        //perchè così li possiamo trattare con il semplice logger::getInstance().metodo()
        //i metodi non statici hanno accesso al puntatore this e quindi sanno quale variabile modificare,
        //mentre i metodi statici non sanno leggere variabili non statiche

};


int main(){

//creiamo una istanza della classe e inzializziamo il valore tramite il metodo pubblico
logger::getInstance().setValore(30);

cout<<"il processo PADRE ha impostato il valore di logger a:  "<< logger::getInstance().stampa_valore()<<endl;


cout<<endl<<"Ora eseguiamo il FORK"<<endl<<endl;

pid_t pid = fork();

if (pid == 0){

    //qui scriviamo il codice del processo figlio

    cout<<"Il FIGLIO creato è una copia del PADRE e quindi avrà il solito valore: "<<logger::getInstance().stampa_valore()<<endl;
    cout<<"ora il FIGLIO decide di cambiare il suo valore a 999"<<endl<<endl;

    logger::getInstance().setValore(999);

    cout<<"FIGLIO afferma che ora nel suo Singleton c' è il valore di logger: "<<logger::getInstance().stampa_valore()<<endl<<endl;

}

//riprendiamo il codice del padre
else if (pid > 0){
    cout<<"Padre aspetta che il figlio agisca per dimostrare che hanno due valori diversi sebbene siano due Singleton, incoerenza perchè ho un solo logger"<<endl<<endl;
    wait(NULL);
    cout<<"Il figlio ha finito!"<<endl<<endl<<endl;

    //facciamo la verifica che, se fosse memoria condivisa avrei ora "valore" = 999 invece ho ancora 30
    cout<<"mostriamo che PADRE e FIGLIO hanno memoria separata"<<endl<<endl;
    cout<<"infatti il valore del padre non  è 999, ma: "<<logger::getInstance().stampa_valore();


    
}





return 0;
}