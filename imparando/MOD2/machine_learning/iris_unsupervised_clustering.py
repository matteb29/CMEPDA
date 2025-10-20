import numpy as np
import seaborn as sns
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA




iris = sns.load_dataset("iris")
iris_np = np.array(iris)


x_iris = iris_np[:, 0: -1]
y_iris = iris_np[:, -1]



model1 = PCA(n_components = 2)

model1.fit(x_iris)

x_2d = model1.transform(x_iris)

iris["PCA1"] = x_2d[:,0]
iris["PCA2"] = x_2d[:,1]


model2 = GaussianMixture(n_components = 3, covariance_type = "full")

#n_components indica il numero di gaussiane distinte che devo trovare nei miei dati
#quindi il numero di cluster che dovrò produrre
#covariance_type = "full" è il metodo più generale che cattura ogni forma del cluster 



model2.fit(x_iris)
#il modello impara su 4dimensioni, quindi su una gaussiana multivariata
#il processo del metodo .fit() è un processo iterativo che si chiama EM che compie le seguenti azioni
#1) i miei dati caratterizzati da 4 features si dispongono su un grafico 5d
#2) fitto questi dati con una gaussina multivariata
#3) disegno in modo casuale (almeno in partenza, poi aggiusterò dopo) delle sezioni di questa gaussiana 
#che saranno delle iperellissoidi (più probabilmente inizia con delle sfere 4dim)
#4) per ogni punto del mio dataset associa ad esso una probabilità di appartenenza ad ognuna di 
#queste iperellissoidi, cioè ogni punto del dataset restituisce un array di probabilità [Pa, Pb, Pc etc]
#5) per ogni ellissoide, sulla base dei valori di probabilità dei punti, assegno ad ogni ellissoide un insieme di punti di appartenenza
#6) date le probabilità di ogni punto del dataset le ellissoidi aggiustano i propri parametri in modo di massimizzare
#le probabilità di appartenza dei punti a loro assegnati 
#7) alla fine del processo ho 3 ellissoidi distinti che contengono diversi punti del dataset 



y_gmm = model2.predict(x_iris)




iris["cluster"] = y_gmm

sns.lmplot( x = "PCA1", y = "PCA2", data = iris, hue = "species", col = "cluster", fit_reg = False)



plt.show()


#notiamo che nei vari cluster i dati delle 3 specie si dispongono in forma di elissoidi
#questo è in accordo con il fatto che i punti di equiprobabilità di una gaussiana multivariata 2dim 
#si dispongono in ellissi
