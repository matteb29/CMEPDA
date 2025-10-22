import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import seaborn as sns


digits = load_digits()

x = digits.data
y = digits.target

x_train,x_test, y_train, y_test = train_test_split(x,y, random_state = 0 )

model = GaussianNB()

model.fit(x_train, y_train) #ricordiamo che GaussianNB lavora facendo
#una gaussiana per ognuna delle feature(qui 64) sui dati di training
#successivamente per ogni test assegna un punteggio alla caratteristica del dato di test
#sulla base di quanto sia probabile

y_model = model.predict(x_test)

accuracy = (sum(y_test == y_model)/len(y_test))
print(accuracy)

print(accuracy_score(y_test, y_model))


#sappiamo che la precisione è dell' 83% tuttavia non sappiamo dove il modello
#sbaglia a classificare, per farcene un' idea usiamo la Confusion Matrix
#che ci dice quante volte un numero predetto viene scambiato per un altro


matrice_confusione = confusion_matrix(y_test, y_model)

sns.heatmap(matrice_confusione, square = True, annot = True, cbar = False)


#annot ci permette di visualizzare in ogni cella quante volte un numero viene
#scambiato per un altro, senza di esso vedo solo una mappa di colore


plt.xlabel("valore predetto")
plt.ylabel("valore vero")

plt.show()



