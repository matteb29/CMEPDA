#ifndef PARTICELLA_H
#define PARTICELLA_H

#include <TObject.h>

class Particella : public TObject {
public:
    int energia;      // I dati che vogliamo salvare
    float posizione;

    // Costruttore
    Particella() { energia = 0; posizione = 0.0; }

    // MACRO FONDAMENTALE PER IL DIZIONARIO
    // Dice a ROOT: "Includi questa classe nel dizionario!"
    ClassDef(Particella, 1); 
};

#endif