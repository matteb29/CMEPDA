#include "Particella.h"
#include "TFile.h"
#include "TTree.h"

void scrivi_dati() {
    // 1. Creiamo il file fisico (.root)
    TFile *file = new TFile("dati_esperimento.root", "RECREATE");

    // 2. Creiamo il TTree (il contenitore)
    TTree *tree = new TTree("albero", "Dati Particelle");

    // 3. Istanziamo l'oggetto e creiamo il Branch
    Particella *p = new Particella();
    
    // Qui avviene la magia: grazie al dizionario, ROOT sa come
    // prendere l'oggetto 'p' e splittarlo nei rami "energia" e "posizione"
    tree->Branch("evento", "Particella", &p);

    // 4. Simuliamo il ciclo di acquisizione dati (es. 1000 eventi)
    for (int i = 0; i < 1000; i++) {
        p->energia = i * 2;         // Dati finti
        p->posizione = i + 0.5;
        
        tree->Fill(); // Serializzazione: copio dalla RAM al Buffer (Basket)
    }

    // 5. Salvataggio finale e chiusura
    file->Write(); // Scrive l'header e i basket rimasti su disco
    file->Close();
}