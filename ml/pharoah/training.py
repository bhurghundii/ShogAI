import numpy as np
import pandas as pd
import itertools
import tensorflow as tf

import math, sys
import logging
logging.basicConfig(level=logging.DEBUG)
import scipy.io as sio # The library to deal with .mat
from sklearn.metrics import classification_report

np.random.seed(1337)  # for reproducibility
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics.classification import accuracy_score
from dbn_v2.tensorflow import SupervisedDBNClassification, UnsupervisedDBN
import datetime

# use "from dbn import SupervisedDBNClassification" for computations on CPU with numpy

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

def dbn_siamese(CSVFILE):
  raw_data = pd.read_csv(CSVFILE)

  Y_LABEL = 'Win'

  KEYS = [i for i in raw_data.keys().tolist() if i != Y_LABEL]
  X = raw_data[KEYS].values
  Y = raw_data[Y_LABEL].values

  class_names = list(raw_data.columns.values)
  print(class_names)


  # Splitting data
  X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=None, shuffle=True, stratify=Y)

  print(X_train)
  print(Y_train)

  # Training
  classifier = SupervisedDBNClassification(hidden_layers_structure=[119, 75, 50, 25],
                                          learning_rate_rbm=0.05,
                                         learning_rate=0.1,
                                         n_epochs_rbm=40,
                                         n_iter_backprop=20,
                                         batch_size=500,
                                         activation_function='relu',
                                         dropout_p=0.2)

  classifier.fit(X_train, Y_train)

  # Save the model
  classifier.save('model.pkl')

  # Restore it
  classifier = SupervisedDBNClassification.load('model.pkl')
  # Test
  Y_pred = classifier.predict(X_test)

  print('Done.\nAccuracy: %f' % accuracy_score(Y_test, Y_pred))
  target_names = ['Win', 'Win']
  print(classification_report(Y_test, Y_pred, target_names=target_names))

dbn_siamese('white_training.csv')