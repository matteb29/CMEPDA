"Vogliamo realizzare una CNN in grado di riconoscere cerchi e rettangoli"

import numpy as np
from matplotlib import pyplot as plt
from keras.layers import Dense, Conv2D, MaxPooling2D, ZeroPadding2D #importo i layers necessari
from keras.models import Model


"Gneriamo delle immagini con figure utilizzando la libreria OpenCV"

import cv2

simple = True
mixed = False
withBB = False


def background():
    return np.zeros((64,64,3), np.uint8) #creo una immagine nera 64X64 poichè riempita di zeri

def randomColor():
  return (int(np.random.rand()*128+128),int(np.random.rand()*128+128),int(np.random.rand()*128+128))


"Generiamo cerchi"
def drawCircle(c, x, y, r):
   
   img = background() #prendiamo la matrice di 0 di dim 64x64 e la chiamiamo img

   cv2.circle(img(x,y), r, c, -1) #al centro di tale matrice di coordinate x, y disegno un cerchio di raggio r 
   #di colore c e riempito (-1), nella pratica i valori degli elementi di matrice che definiscono il cerchio
   #cambiano da 0 a c 

   return img, x-r, y-r, x+r, y+r #oltre all' immagine ci facciamo restituire le 4 coordinate della bounding box
    #nota che l' immagine è la matrice 64x64 con entries modificate

#funzione per generare i cerchi
def genCircle():
  
  return drawCircle(randomColor(),int(np.random.rand()*50)+10,int(np.random.rand()*50)+10, int(np.random.rand()*6)+3)


"Generiamo i rettangoli"
def drawRectangle(c, x, y, w, h):
   img = background()
   cv2.rectangle(img(x,y), (x+w), (y+h), c, -1)
   return img, x, y, x+w, y+h #mi faccio sempre restituire le coordinate di due estremi opposti di un rettangolo: bounding box

def genRectangle():
   return drawRectangle(randomColor(), int(np.random.rand()*40)+ 10, int(np.random.rand()*40)+10, int(np.random.rand()*6)+3, int(np.random.rand()*6)+3)



"Creiamo una funzione per gestire più figure"

#f sarà la funzione che genera la figura, i è il numero di figure all' interno dell' immagine
def genN(f, i):
   
   img_bkg = np.zeros((64, 64, 3), np.uint8) #uint 8 significa numero a 8 bit che equivale ad un numero da 0 a 255

   for x in range(i):
      
      img_bkg += f()[0] #riconduco la creiazione di nuove figure in una immagine
      #alla somma di specifici numeri nella matrice di bkg in base alla componente 0 di f
      #notiamo che f è una funzione drawRectangle che restituisce 4 oggetti di cui la componente 0 è l' 
      # immagine con il rettangolo

   return img_bkg


nsamples = 100

if simple : 
   
   targets = np.random.rand(nsamples)>0.5 #ho un arrey di 100 numeri casuali tra 0 e 1 che viene confrontato con 0. 5
   #ottengo alla fine un array di lunghezza 100 contenente True or False


    #ciclo for rapido in cui genero 100 immagini in base alla entry target[x] sia True or False
   images = np.array([genCircle()[0]] if targets[x] else genRectangle()[0] for x in range(nsamples))


if mixed : 
   
   #creo una matrice 100 x 2 fatta di numeri casuali tra 0 e 4
   #ogni riga sarà il numero di cerchi e il numero di rettangoli da disegnare
   targets = np.stack( np.random.rand(nsamples)*4, np.random.rand(nsamples)*4, axis = 1) 

   #trasforma l' array targets in un array di interi mentre prima il numero di cerchi e rettangoli era un decimale
   targets = np.array(targets, dtype = int)

   images = np.array([genN(genRectangle, targets[x, 0] ) + genN(genCircle, targets[x, 1]) for x in range(nsamples)])
                     


