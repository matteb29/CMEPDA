import time

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from matplotlib.colors import ListedColormap

np.random.seed(123)

theFunction = lambda x1, x2: np.sin(x1 * 20) > x2 * x2 - x1

N = 3000
x1 = 1.0 * np.random.rand(N)
x2 = 1.0 * np.random.rand(N)
ynp = theFunction(x1, x2)

print(x1[:10])
print(x2[:10])
Xnp = np.stack((x1, x2), axis=1)

print(x1)
print(x2)
print(Xnp)
print(ynp)


cm_bright = ListedColormap(["#FF0000", "#0000FF"])
plt.scatter(Xnp[:, 0], Xnp[:, 1], c=ynp, cmap=cm_bright, edgecolors="k")


xx1, xx2 = np.meshgrid(np.arange(0, 1, 0.01), np.arange(0, 1, 0.01))
plt.contourf(
    xx1, xx2, (theFunction(xx1, xx2)).reshape(xx1.shape), cmap=plt.cm.RdBu, alpha=0.8
)

X = torch.tensor(Xnp, dtype=torch.float32).to("cpu")
y = torch.tensor(ynp, dtype=torch.float32).reshape(-1, 1).to("cpu")
print(X)
print(y)


class MySimpleDNN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(2, 50)
        self.layer2 = nn.Linear(50, 50)
        self.layer3 = nn.Linear(50, 50)
        self.output = nn.Linear(50, 1)

    def forward(self, x):
        h = self.layer1(x)
        h = h.relu()
        h = self.layer2(h)
        h = h.relu()
        h = self.layer3(h)
        h = h.relu()
        h = self.output(h)
        h = torch.sigmoid(h)
        return h


model = MySimpleDNN().to("cpu")
print(model)
print([x for x in model.parameters()])
loss_fn = nn.BCELoss()  # binary cross entropy
optimizer = optim.Adam(model.parameters(), lr=0.002)

n_epochs = 400
batch_size = 128
loss_history = []
for epoch in range(n_epochs):
    starttime = time.time()
    for i in range(0, len(X), batch_size):
        Xbatch = X[i : i + batch_size]
        y_pred = model(Xbatch)
        ybatch = y[i : i + batch_size]
        loss = loss_fn(y_pred, ybatch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(
        f"Finished epoch {epoch},latest loss {loss} in",
        time.time() - starttime,
        "seconds",
    )
    loss_history.append(loss.cpu().detach().numpy())

plt.figure()
plt.plot(loss_history)
plt.show()
