import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
import seaborn as sns
#iris = load_iris()
#data = pd.DataFrame(iris.data, columns=iris.feature_names)
df = sns.load_dataset("iris")

print(df.shape)
#print(data.shape)

x = np.arange(0,10,0.1)
y = x*x

plt.plot(x,y)
plt.title("sample_graph")
plt.xlabel("x")
plt.ylabel("y")
plt.show()