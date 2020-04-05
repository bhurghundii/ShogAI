import pandas as pd
df = pd.read_csv('black_training_2.csv')
df.Win = 0
df.to_csv('black_training_tmp.csv', index=False, sep=',')

df = pd.read_csv('white_training_2.csv')
df.Win = 1
df.to_csv('white_training_tmp.csv', index=False, sep=',')