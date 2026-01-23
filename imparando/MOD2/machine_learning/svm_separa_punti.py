import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.datasets import make_blobs  # serve per creare dati finti
from sklearn.svm import SVC

x, y = make_blobs(
    n_samples=100, centers=2, random_state=0, cluster_std=0.60
)  # creiamo 50 punti suddivisi in 2 gruppi
# i centers sono i gruppi di punti

plt.scatter(x[:, 0], x[:, 1], c=y, s=50, cmap="autumn")


model = SVC(kernel="linear", C=1e10)
# kernel = linear signfica che dobbiamo trovare una linea retta
# c mi dice quanto deve essere rigido il modello


model.fit(x, y)
# terminato il processo di addestramento con model.fit il modello ha dentro di se la retta che
# divide i due punti


# facciamo una predizione su un nuovo punto casuale
nuovo_punto = [[1, 3]]
predizione_modello = model.predict(nuovo_punto)
print(predizione_modello)


# creiamo una funzione per mostrare cosa fa svc


def plot_svc_decisione(model, ax=None, plot_support=True):

    if ax is None:
        ax = plt.gca()  # plt.gca è l' asse attivo cioè
        # se non specifico alcun asse devo prendere come ax l' asse attivo
        # con asse attivo si intende l'area specifica del grafico su cui matplotlib sta "lavorando" in un dato momento.
        # in matplotlib, la parola Axes si riferisce all'intera area di disegno rettangolare

    xlim = (
        ax.get_xlim()
    )  # con questo imposto xlim uguale al bordo x dell' area su cui sta lavorando
    ylim = ax.get_ylim()  # e con questo imposto il bordo y

    # create grid to evaluate model
    x_lin = np.linspace(
        xlim[0], xlim[1], 30
    )  # creo 30 punti equispaziati sull' asse x a partire da
    y_lin = np.linspace(ylim[0], ylim[1], 30)

    Y, X = np.meshgrid(
        y_lin, x_lin
    )  # creo una griglia 30x30 cioè 900 punti, che copra l' intera area del grafico

    xy = np.vstack([X.ravel(), Y.ravel()]).T  # creo una griglia xy

    # qui invoco il metodo decision_function sulla griglia xy
    P = model.decision_function(xy).reshape(X.shape)

    # plot decision boundary and margins
    ax.contour(
        X, Y, P, colors="k", levels=[-1, 0, 1], alpha=0.5, linestyles=["--", "-", "--"]
    )

    # plot support vectors
    if plot_support:
        ax.scatter(
            model.support_vectors_[:, 0],
            model.support_vectors_[:, 1],
            s=300,
            linewidth=1,
            edgecolors="black",
            facecolors="none",
        )

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


plot_svc_decisione(model)
plt.show()


# i support vector sono i dati che toccano i margini della linea che separa i due set di dati
print(model.support_vectors_)
