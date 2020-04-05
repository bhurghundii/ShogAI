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
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import layers
from sklearn.utils import shuffle
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras import regularizers
from tensorflow.keras.optimizers import Adam
import random 

tf.compat.v1.disable_eager_execution()
np.set_printoptions(precision=3)

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

random.seed(100)

full_data_black = pd.read_csv('black_training_3.csv', nrows=5000)
full_data_white = pd.read_csv('white_training_3.csv', nrows=5000)

#20295

third_dataset = pd.concat([full_data_black, full_data_white], ignore_index=True, sort =False)
raw_data_black = full_data_black
raw_data_white = full_data_white


Y_LABEL = 'Win'

KEYS = [i for i in raw_data_black.keys().tolist() if i != Y_LABEL]
third_features = third_dataset[KEYS].values


third_labels = third_dataset[Y_LABEL].values

third_train_x, third_test_x, third_train_y, third_test_y = train_test_split(third_features, third_labels, test_size=0.3, shuffle=True)


num_neurons1 = third_train_x.shape[1]

encoding_dim1 = 1500
encoding_dim4 = 750
encoding_dim5 = 200

input_data = Input(shape=(num_neurons1,))
encoded = Dense(encoding_dim1, activation='relu', name='encoder1')(input_data)
encoded3 = Dense(encoding_dim4, activation='relu', name='encoder4')(encoded)
encoded4 = Dense(encoding_dim5, activation='relu', name='encoder5')(encoded3)

decoded4 = Dense(encoding_dim5, activation='relu', name='decoder2')(encoded4)
decoded3 = Dense(encoding_dim4, activation='relu', name='decoder3')(decoded4)
decoded0 = Dense(encoding_dim1, activation='relu', name='decoder6')(decoded3)
decoded = Dense(num_neurons1, activation='sigmoid', name='decoder')(decoded0)

# this model maps an input to its reconstruction
autoencoder1 = Model(inputs=input_data, outputs=decoded)
autoencoder1.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# training
autoencoder1.fit(third_train_x, third_train_x,
                    epochs=200, #200 for final with early stopping
                    shuffle=True,
                    validation_data=(third_test_x, third_test_x))


autoencoder_black = Model(inputs=autoencoder1.inputs, outputs=autoencoder1.layers[-5].output)
autoencoder_black.summary()
autoencoder_black.save('autoencoder_black.h5')

numpyOutputFromAuto1 = autoencoder_black.predict(third_train_x)


scalar = MinMaxScaler()
#Scale win autoencoder for black
numpyOutputFromAuto1 = scalar.fit_transform(numpyOutputFromAuto1)


inputDataForThird = numpyOutputFromAuto1

inputTensorForMlp = Input(shape=(200,))

h = Dense(64, activation='relu', name='hidden')(inputTensorForMlp)
h3 = Dense(32, activation='relu', name='hidden1')(h)
out = Dense(1, activation='sigmoid', name='prediction')(h3)

model = Model(inputs=inputTensorForMlp, outputs=out)
adamOpt = Adam(lr=0.00001, decay=1e-6)

model.compile(loss='binary_crossentropy', optimizer=adamOpt, metrics=['accuracy'])

#5000 for final
model.fit(inputDataForThird ,third_train_y , epochs=5000, shuffle=True)

model.save("model_single.h5")
print("Saved model to disk")

print(model.summary())

test_black = autoencoder_black.predict(third_test_x)
scalar = MinMaxScaler()
#Scale win autoencoder for black
test_black = scalar.fit_transform(test_black)

#Scale win autoencoder for white

preds = model.predict(np.concatenate([test_black],axis=-1))
labels = (preds < 0.5).astype(np.int)


b = 1-third_test_y
labelsForThird = np.column_stack((third_test_y,b))
target_names = ['Win', 'Loss']
print(accuracy_score(labels, b))
