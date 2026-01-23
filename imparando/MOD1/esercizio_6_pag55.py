import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame, Series

url = "https://data.cityofnewyork.us/api/views/kxp8-n2sj/rows.csv?accessType=DOWNLOAD"


df = pd.read_csv(url)

print(df.head())
plt.hist(df["passenger_count"], bins=20, color="blue", alpha=0.8)
plt.xlabel("Numero di passggeri")
plt.ylabel("Frequenza")

plt.title("Istogramma del numero di passeggeri nei taxi a New York")

plt.show()
