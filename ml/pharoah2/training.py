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
'''
raw_data_black_head = full_data_black.head(1000)
raw_data_white_head = full_data_white.head(1000)

raw_data_black_tail = full_data_black.tail(1000)
raw_data_white_tail = full_data_white.tail(1000)

raw_data_black = pd.concat([raw_data_black_head, raw_data_black_tail], ignore_index=True, sort =False)
raw_data_white = pd.concat([raw_data_white_head, raw_data_white_tail], ignore_index=True, sort =False)
'''

raw_data_black = full_data_black
raw_data_white = full_data_white

mincut= min(len(raw_data_black), len(raw_data_white))

#Data cleaning
raw_data_black = raw_data_black[raw_data_black['Win'].notna()]
raw_data_white = raw_data_white[raw_data_white['Win'].notna()]

#Keep it the same size...
raw_data_black = raw_data_black[:mincut]
raw_data_white = raw_data_white[:mincut]

#Shuffle in the same way
idx = np.random.permutation(raw_data_black.index)

raw_data_black = raw_data_black.reindex(idx)
raw_data_white = raw_data_white.reindex(idx)

third_dataset = pd.concat([raw_data_black, raw_data_white], ignore_index=True, sort =False)

Y_LABEL = 'Win'

KEYS = [i for i in raw_data_black.keys().tolist() if i != Y_LABEL]
x_black = raw_data_black[KEYS].values
x_white = raw_data_white[KEYS].values
third_features = third_dataset[KEYS].values

Y_black = raw_data_black[Y_LABEL].values
Y_white = raw_data_white[Y_LABEL].values
third_labels = third_dataset[Y_LABEL].values


num_neurons1 = x_black.shape[1]
num_neurons2 = x_white.shape[1]

print(len(x_white), len(x_black), len(Y_black), len(Y_white))

# Train-test split
x_black_train, x_black_test, y_black_train, y_black_test = train_test_split(x_black, Y_black, test_size=0.3, shuffle=True)
x_white_train, x_white_test, y_white_train, y_white_test = train_test_split(x_white, Y_white, test_size=0.3,  shuffle=True)



# scale data within [0-1] range
scalar = MinMaxScaler()
#Scale win autoencoder for black
x_black_train = scalar.fit_transform(x_black_train)
x_black_test = scalar.transform(x_black_test)

#Scale win autoencoder for white
x_white_train = scalar.fit_transform(x_white_train)
x_white_test = scalar.transform(x_white_test)

softmax_black = 1-y_black_train

softmax_white = 1-y_white_train

y_black_train = np.concatenate([softmax_black,y_black_train], axis=-1)
y_white_train = np.concatenate([y_white_train,softmax_white], axis=-1)

print (y_black_train.shape)
print (y_white_train.shape)

encoding_dim1 = 3000
encoding_dim4 = 750
encoding_dim5 = 100

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
autoencoder1.fit(x_black_train, x_black_train,
                    epochs=5, #200 for final with early stopping
                    shuffle=True,
                    validation_data=(x_black_test, x_black_test))


autoencoder_black = Model(inputs=autoencoder1.inputs, outputs=autoencoder1.layers[-5].output)
autoencoder_black.summary()
autoencoder_black.save('autoencoder_black.h5')

encoding_dim1 = 3000
encoding_dim4 = 750
encoding_dim5 = 100

input_data = Input(shape=(num_neurons2,))
encoded = Dense(encoding_dim1, activation='relu', name='encoder1')(input_data)
encoded3 = Dense(encoding_dim4, activation='relu', name='encoder4')(encoded)
encoded4 = Dense(encoding_dim5, activation='relu', name='encoder5')(encoded3)

decoded4 = Dense(encoding_dim5, activation='relu', name='decoder2')(encoded4)
decoded3 = Dense(encoding_dim4, activation='relu', name='decoder3')(decoded4)
decoded0 = Dense(encoding_dim1, activation='relu', name='decoder6')(decoded3)
decoded = Dense(num_neurons1, activation='sigmoid', name='decoder')(decoded0)


# this model maps an input to its reconstruction
autoencoder2 = Model(inputs=input_data, outputs=decoded)
autoencoder2.compile(optimizer='adam', loss='binary_crossentropy' , metrics=['accuracy'])

# training
autoencoder2.fit(x_white_train, x_white_train,
                    epochs=5, #200 for final
                    shuffle=True,
                    validation_data=(x_white_test, x_white_test))
#autoencoder1.save("autoencoder_white.h5")

autoencoder_white = Model(inputs=autoencoder2.inputs, outputs=autoencoder2.layers[-5].output)
autoencoder_white.summary()
autoencoder_white.save('autoencoder_white.h5')



third_train_x, third_test_x, third_train_y, third_test_y = train_test_split(third_features, third_labels, test_size=0.3, shuffle=True)
print (third_train_x.shape)
print (third_train_y.shape)


numpyOutputFromAuto1 = autoencoder_black.predict(third_train_x)
numpyOutputFromAuto2 = autoencoder_white.predict(third_train_x)

scalar = MinMaxScaler()
#Scale win autoencoder for black
numpyOutputFromAuto1 = scalar.fit_transform(numpyOutputFromAuto1)

#Scale win autoencoder for white
numpyOutputFromAuto2 = scalar.fit_transform(numpyOutputFromAuto2)


inputDataForThird = np.concatenate([numpyOutputFromAuto1,numpyOutputFromAuto2], axis=-1)
#yinputsForThird = np.concatenate([y_black_train.reshape(-1,1),y_white_train.reshape(-1,1),],axis=-1)
b = 1-third_train_y
labelsForThird = np.column_stack((third_train_y,b))

print (inputDataForThird.shape)

inputTensorForMlp = Input(shape=(200,))
#kernel_regularizer=regularizers.l2(0.1), activity_regularizer=regularizers.l1(0.1)

h = Dense(64, activation='relu', name='hidden')(inputTensorForMlp)
h2 = Dropout(0.2)(h)
h3 = Dense(32, activation='relu', name='hidden1')(h2)
#h4 = Dropout(0.3)
out = Dense(2, activation='softmax', name='prediction')(h3)

model = Model(inputs=inputTensorForMlp, outputs=out)
adamOpt = Adam(lr=1e-6)

model.compile(loss='categorical_crossentropy', optimizer=adamOpt, metrics=['accuracy'])

#5000 for final
model.fit(inputDataForThird ,labelsForThird , epochs=5000, shuffle=True, batch_size=128)


preds = model.predict(np.concatenate([autoencoder_black.predict(third_test_x),autoencoder_white.predict(third_test_x)],axis=-1))

tf.summary.histogram("predictions", preds)
model.save("model_test.h5")
print("Saved model to disk")

print(model.summary())



test_black = autoencoder_black.predict(third_test_x)
test_white = autoencoder_white.predict(third_test_x)
scalar = MinMaxScaler()
#Scale win autoencoder for black
test_black = scalar.fit_transform(test_black)

#Scale win autoencoder for white
test_white = scalar.fit_transform(test_white)

preds = model.predict(np.concatenate([test_black,test_white],axis=-1))
labels = (preds < 0.5).astype(np.int)

b = 1-third_test_y
labelsForThird = np.column_stack((third_test_y,b))
target_names = ['Win', 'Loss']
print(accuracy_score(labels, labelsForThird))