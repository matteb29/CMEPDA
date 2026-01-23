"""
se non usassi la lambda function dovrei fare una funzione contatore fuori ed usare una struct(una classe che contiene solo dati,
un dato che contiene altri dati) per importare la variabile da incrementare da fuori a dentro il main.
Questa struct non deve contenere solo dati, ma deve anche contenere il codice per 
comportarsi come una funzione (in C++ si chiama Funtore).

sarebbe stato 

#include <iostream>
#include <vector>
#include <algorithm>

// 1. Dobbiamo creare una STRUCT apposta per fare questo lavoro
struct Controllore {
    // A. La "tasca" per nascondere la variabile del main
    int sogliaSegreta; 

    // B. Il costruttore per mettere la variabile nella tasca
    Controllore(int s) {
        sogliaSegreta = s;
    }

    // C. Il trucco magico (operator):
    // Questo permette alla struct di essere chiamata come una funzione: f(x)
    void operator()(int n) {
        if (n > sogliaSegreta) { // Usa la variabile nascosta!
            std::cout << n << " e' maggiore di " << sogliaSegreta << std::endl;
        }
    }
};

int main() {
    std::vector<int> numeri = {10, 60, 20, 90};
    int sogliaMain = 50; // Variabile che voglio passare

    // 2. Preparo il "trasportino" (l'oggetto funtore)
    Controllore ilMioOggetto(sogliaMain); 

    // 3. Lo passo all'algoritmo
    // L'algoritmo crede di chiamare una funzione, ma sta chiamando la struct!
    std::for_each(numeri.begin(), numeri.end(), ilMioOggetto);
    
    return 0;
}



"""

#include <iostream>

int main() {
    // 1. Variabile nel "blocco chiamante" (main)
    int contatore = 0; 

    // 2. Definizione Lambda
    // [&contatore] -> "Prendi il contatore vero (riferimento) per poterlo modificare"
    auto incrementa = [&contatore]() {
        contatore++; // Modifica la variabile esterna!
    };

    // 3. Esecuzione
    incrementa(); // contatore diventa 1
    incrementa(); // contatore diventa 2

    std::cout << "Valore finale: " << contatore << std::endl; // Stampa 2
    return 0;
}