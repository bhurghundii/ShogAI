import pandas as pd 

df = pd.read_csv('features.csv', header=None)
ds = df.sample(frac=1)
print(ds)

ds.to_csv('newfile.csv')