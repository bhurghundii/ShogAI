import pandas as pd
df = pd.read_csv("training.csv")

df = df[pd.notnull(df['Win'])]

df.to_csv("training_2.csv", index=False, sep=',')

