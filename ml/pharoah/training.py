import tensorflow as tf
import numpy as np
import pandas as pd
import datetime
import itertools
import logging
import math
import sys

import numpy as np
import pandas as pd
import scipy.io as sio  # The library to deal with .mat
import tensorflow as tf
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.classification import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense, Input, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras import layers

tf.compat.v1.disable_eager_execution()
num_hidden=100

def get_dataset(file_path, **kwargs):
  dataset = tf.data.experimental.make_csv_dataset(
      file_path,
      batch_size=5000, # Artificially small to make examples easier to show.
      label_name='Win',
      na_value="?",
      num_epochs=1,
      ignore_errors=True, 
      **kwargs)
  return dataset

def show_batch(dataset):
  for batch, label in dataset.take(1):
    for key, value in batch.items():
      print("{:20s}: {}".format(key,value.numpy()))

def pack(features, label):
  return tf.stack(list(features.values()), axis=-1), label


raw_data = pd.read_csv('training.csv')

Y_LABEL = 'Win'

KEYS = [i for i in raw_data.keys().tolist() if i != Y_LABEL]
X1 = raw_data[KEYS].values
X2 = raw_data[KEYS].values

Y = raw_data[Y_LABEL].values

num_neurons1 = X1.shape[1]
num_neurons2 = X2.shape[1]

# Train-test split
x1_train, x1_test, x2_train, x2_test, y_train, y_test = train_test_split(X1, X2, Y, test_size=0.2)

# scale data within [0-1] range

scalar = MinMaxScaler()
x1_train = scalar.fit_transform(x1_train)
x1_test = scalar.transform(x1_test)

x2_train = scalar.fit_transform(x2_train)
x2_test = scalar.transform(x2_test)

x_train = np.concatenate([x1_train, x2_train], axis =-1)
x_test = np.concatenate([x1_test, x2_test], axis =-1)

encoding_dim1 = 500
encoding_dim2 = 100

input_data = Input(shape=(num_neurons1,))
encoded = Dense(encoding_dim1, activation='relu', name='encoder1')(input_data)
encoded1 = Dense(encoding_dim2, activation='relu', name='encoder2')(encoded)
decoded = Dense(encoding_dim2, activation='relu', name='decoder1')(encoded1)
decoded = Dense(num_neurons1, activation='sigmoid', name='decoder2')(decoded)

# this model maps an input to its reconstruction
autoencoder1 = Model(inputs=input_data, outputs=decoded)
autoencoder1.compile(optimizer='sgd', loss='mse')                                                                                                                                                                                                                                                                                                                                                                                                 
# training
autoencoder1.fit(x1_train, x1_train,
                    epochs=200,
                    batch_size=300,
                    shuffle=True,
                    validation_data=(x1_test, x1_test))


encoding_dim1 = 500
encoding_dim2 = 100

input_data = Input(shape=(num_neurons2,))
encoded = Dense(encoding_dim1, activation='relu', name='encoder1')(input_data)
encoded2 = Dense(encoding_dim2, activation='relu', name='encoder2')(encoded)
decoded = Dense(encoding_dim2, activation='relu', name='decoder1')(encoded2)
decoded = Dense(num_neurons2, activation='sigmoid', name='decoder2')(decoded)


# this model maps an input to its reconstruction
autoencoder2 = Model(inputs=input_data, outputs=decoded)
autoencoder2.compile(optimizer='sgd', loss='mse')

# training
autoencoder2.fit(x2_train, x2_train,
                    epochs=200,
                    batch_size=300,
                    shuffle=True,
                    validation_data=(x2_test, x2_test))

numpyOutputFromAuto1 = autoencoder1.predict(x1_train)    
numpyOutputFromAuto2 = autoencoder2.predict(x2_train)

inputDataForThird = np.concatenate([numpyOutputFromAuto1,numpyOutputFromAuto2],axis=-1)

inputTensorForMlp = Input(shape=(6664,))
h = Dense(100, activation='relu', name='hidden')(inputTensorForMlp)
y = Dense(1, activation='sigmoid', name='prediction')(h)

mymlp = Model(inputs=inputTensorForMlp, outputs=y)

mymlp.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

mymlp.fit(inputDataForThird ,Y[:1178], epochs=200)

preds = mymlp.predict(inputDataForThird)

class_one = preds > 0.5

acc = np.mean(class_one == Y[:1178])
print(acc)

mymlp.save("model.h5")
print("Saved model to disk")