#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm> //per std::copy
using namespace std;


class Array{

    int* data;
    size_t size;

    public:

        //il costruttore per realizzare istanze
        Array(size_t size){
            this->size = size;
            this->data = new int[size];
        }

        //il distruttore per eliminare l' array
        ~Array(){
            delete[] data;
        }

        //il costruttore della copia
        Array(const Array& array_da_copiare) //: size(array_da_copiare.size) modo rapido per fare assegnazione
        {

            size = array_da_copiare.size;

            //allochiamo nuova memoria così vivono in due spazi diversi oggetto e sua copia
            data = new int[array_da_copiare.size];

            //copia
            std::copy(array_da_copiare.data, array_da_copiare.data + array_da_copiare.size, data);


        }

        //operatore di assegnazione, restituisce il puntatore all' array con i dati copiati
        Array& operator=(const Array& array_da_copiare){
        if (this == &array_da_copiare) return *this; // Protezione da auto-assegnazione (a = a)
        //cioè se il puntatore all' oggetto che si sta utilizzando punta al solito indirizzo dell' array da copire
        //ci facciamo restituire i dati contenuti 

        //altrimenti..
        delete[] data;                    //  Pulisco la mia vecchia memoria
        
        //copio la dimensione
        size = array_da_copiare.size;
        data = new int[array_da_copiare.size];       // 2. Alloco NUOVA memoria
        std::copy(array_da_copiare.data, array_da_copiare.data + array_da_copiare.size, data); // 3. Copio i valori
        
        return *this;
    }

};


int main(){

    //testiamo che funzioni tutto

    Array a(10);
    Array b = a;

    {
        cout << "\n--- 2. Creo B (copia di A) dentro uno scope ---" << endl;
        Array b = a; 
        
        // Modifico B per provare che sono diversi
        b.data[0] = 999; 
        
        cout << "Indirizzo dati A: " << a.data << " | Valore[0]: " << a.data[0] << endl;
        cout << "Indirizzo dati B: " << b.data << " | Valore[0]: " << b.data[0] << endl;
        
        cout << "\n--- 3. B sta per morire (fine parentesi graffa) ---" << endl;
    } 
    // QUI scatta il distruttore di B automaticamente!
    
    cout << "\n--- 4. Siamo tornati nel main. B è morto. ---" << endl;
    
    // RISPOSTA ALLA TUA DOMANDA:
    cout << "Esiste ancora A? SI!" << endl;
    cout << "Indirizzo dati A: " << a.data << endl;
    cout << "Valore[0] di A: " << a.data[0] << " (Deve essere ancora 1, non 999)" << endl;

    return 0;
}
