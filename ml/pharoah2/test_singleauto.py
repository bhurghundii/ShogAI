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

full_data_black = pd.read_csv('black_training_3.csv', nrows=1000)
full_data_white = pd.read_csv('white_training_3.csv', nrows=1000)

#20295

third_dataset = pd.concat([full_data_black, full_data_white], ignore_index=True, sort =False)
raw_data_black = full_data_black
raw_data_white = full_data_white


Y_LABEL = 'Win'

KEYS = [i for i in raw_data_black.keys().tolist() if i != Y_LABEL]
third_features = third_dataset[KEYS].values


third_labels = third_dataset[Y_LABEL].values

third_train_x, third_test_x, third_train_y, third_test_y = train_test_split(third_features, third_labels, test_size=0.3, shuffle=True)


autoencoder_black = load_model('autoencoder.h5')
model = load_model('model_single.h5')

test_black = autoencoder_black.predict(third_test_x)
scalar = MinMaxScaler()
#Scale win autoencoder for black
test_black = scalar.fit_transform(test_black)

#Scale win autoencoder for white

preds = model.predict(np.concatenate([test_black],axis=-1))
print(preds)
labels = (preds < 0.5).astype(np.int)

b = 1-labels
labelsForThird = np.column_stack((third_test_y,b))
target_names = ['Win', 'Loss']
print(accuracy_score(b, third_test_y))
print(b)
print(third_test_y)
print(preds)
