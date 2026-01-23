#include <iostream>
using namespace std;

class Robot {
private:
    int id_personale; // Variabile normale (offset relativo)

public:
    static int frequenza_radio; // Variabile static (assoluta)
    //quando scrivo static sto dicendo che questa variabile non dovrà 
    //mai vivere in uno spazio di memoria dedicato alla singola istanza






    // 1. IL COSTRUTTORE E L'OMONIMIA
    // Qui usiamo 'this' per distinguere il parametro dalla variabile interna
    Robot(int id_personale) {
        // id_personale = id_personale; // SBAGLIATO! Assegna il parametro a se stesso
        
        this->id_personale = id_personale; 
        // "Il MIO (this) id diventa uguale al parametro id"
    }

    // 2. METODO NORMALE (Ha il 'this')
    void chiSono() {
        cout << "--- DENTRO IL METODO chiSono() ---" << endl;
        
        // Stampiamo il valore del puntatore 'this'
        cout << "Il mio indirizzo 'this' e': " << this << endl;
        
        // Posso accedere alla variabile perché so dove sono (this + offset)
        cout << "Il mio ID e': " << this->id_personale << endl;
    }

    // 3. METODO STATIC (NON ha il 'this')
    static void broadcast() {
        cout << "--- DENTRO IL METODO STATIC broadcast() ---" << endl;

        // OK: Posso leggere variabili statiche (sono globali)
        cout << "Frequenza radio: " << frequenza_radio << " MHz" << endl;

        // ERRORE FATALE: PROVARE A USARE 'this' O VARIABILI NORMALI
        // Se scommenti le righe sotto, il compilatore esplode:
        
        // cout << this; 
        // Errore: "'this' is unavailable for static member functions"
        
        // cout << id_personale; 
        // Errore: "invalid use of member 'id_personale' in static member function"
        // (Perché manca il 'this' per trovarlo!)
    }
};




// Inizializzazione statica fuori dalla classe
int Robot::frequenza_radio = 101;






int main() {
    // Creiamo due robot in posti diversi della memoria
    Robot r1(10);
    Robot r2(20);

    cout << "=== ANALISI ROBOT 1 ===" << endl;
    // Stampiamo l'indirizzo di r1 dal main
    cout << "Indirizzo di r1 nel main:  " << &r1 << endl;
    // Chiamiamo il metodo che stampa 'this'
    r1.chiSono();

    cout << "\n=== ANALISI ROBOT 2 ===" << endl;
    // Stampiamo l'indirizzo di r2 dal main
    cout << "Indirizzo di r2 nel main:  " << &r2 << endl;
    r2.chiSono();

    cout << "\n=== PROVA STATIC ===" << endl;
    // Chiamiamo la funzione statica (senza oggetto)
    Robot::broadcast();

    return 0;
}