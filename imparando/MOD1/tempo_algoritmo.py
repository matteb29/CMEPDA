import datetime

import matplotlib.pytplot as plt
import numpy as np

t0 = datetime.datetime.now()

for c in range (20):
    for i in range(1000):
    t1 = datetime.datetime.now()
    t = t1-t0



print(f"tempo impiegato: {t} ")












import datetime

import matplotlib.pyplot as plt
import numpy as np

x=[]
for j in range(1000):
    t0=datetime.datetime.now()
    for i in range(j):
        i+=1
        for z in range(i):
            z+=1
        
    t1=datetime.datetime.now()
    delta=t1-t0
    x.append(delta)
#convertiamo in microsecondi
microsecond=[delta.total_seconds() * 1000000 for delta in x]   
print(microsecond)
y=np.linspace(0,1000,1000)
plt.xlabel('samples')
plt.ylabel('microseconds')
plt.plot(y,microsecond,color='black',marker='o')
plt.show()