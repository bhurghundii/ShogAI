import pandas as pd
df = pd.read_csv("black_training.csv")

df = df[pd.notnull(df['Win'])]

df.to_csv("black_training_2.csv", index=False, sep=',')


df = pd.read_csv("white_training.csv")

df = df[pd.notnull(df['Win'])]

df.to_csv("white_training_2.csv", index=False, sep=',')
