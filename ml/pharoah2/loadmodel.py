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
from sklearn.utils import shuffle
from tensorflow.keras.models import load_model
import random 

from sklearn.metrics import classification_report

tf.compat.v1.disable_eager_execution()

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

raw_data_black = pd.read_csv('black_training_3.csv', nrows=1000)
raw_data_white = pd.read_csv('white_training_3.csv', nrows=1000)
mincut= min(len(raw_data_black), len(raw_data_white))

#Data cleaning
raw_data_black = raw_data_black[raw_data_black['Win'].notna()]
raw_data_white = raw_data_white[raw_data_white['Win'].notna()]

#Keep it the same size...
raw_data_black = raw_data_black[:mincut]
raw_data_white = raw_data_white[:mincut]

Y_LABEL = 'Win'

KEYS = [i for i in raw_data_black.keys().tolist() if i != Y_LABEL]
x_black = raw_data_black[KEYS].values
x_white = raw_data_white[KEYS].values

Y_black = raw_data_black[Y_LABEL].values
Y_white = raw_data_white[Y_LABEL].values

num_neurons1 = x_black.shape[1]
num_neurons2 = x_white.shape[1]

print(len(x_white), len(x_black), len(Y_black), len(Y_white))

# Train-test split
x_black_train, x_black_test, y_black_train, y_black_test = train_test_split(x_black, Y_black, test_size=0.3, random_state=123)
x_white_train, x_white_test, y_white_train, y_white_test = train_test_split(x_white, Y_white, test_size=0.3, random_state=123)

# scale data within [0-1] range
scalar = MinMaxScaler()
#Scale win autoencoder for black
x_black_train = scalar.fit_transform(x_black_train)
x_black_test = scalar.transform(x_black_test)

#Scale win autoencoder for white
x_white_train = scalar.fit_transform(x_white_train)
x_white_test = scalar.transform(x_white_test)


print(len(y_black_train), len(y_white_train))

model = load_model('model2.h5')
preds = model.predict(np.concatenate([x_black_test,x_black_test],axis=-1))

y_classes = preds.argmax(axis=-1)

print(y_classes)
target_names = ['Black', 'White']
print(classification_report(y_black_test, y_classes, target_names=target_names))

