import numpy as np

numeri = np.random.rand(100)  # questi da una uniforme tra 0 e 1
numeri_gauss = np.random.normal(
    0, 1, 100000
)  # questi da una gaussiana con media 0 e dev std 1
# (media, dev std, dimensione campione)

somma = np.sum(numeri)
media = np.mean(numeri)
radice = np.sqrt(np.mean(numeri**2))


somma_gauss = np.sum(numeri_gauss)
media_gauss = np.mean(numeri_gauss)
deviazione_gauss = np.std(numeri_gauss)


deviazione_standard = np.std(numeri)


print(
    f"somma: {somma:.2f}, media: {media:.2f}, deviazione standard: {deviazione_standard:.2f}, radice: {radice:.2f}"
)
print(
    f"somma gauss: {somma_gauss:.2f}, media gauss: {media_gauss:.2f}, deviazione gauss: {deviazione_gauss:.2f}"
)
