
import datetime
import itertools
import logging
import math
import sys

import numpy as np
import pandas as pd
import scipy.io as sio  # The library to deal with .mat
import tensorflow as tf
from dbn_v2.tensorflow import SupervisedDBNClassification, UnsupervisedDBN
from sklearn.datasets import load_digits
from sklearn.metrics import classification_report
from sklearn.metrics.classification import accuracy_score
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.DEBUG)

np.random.seed(1337)  # for reproducibility
tf.compat.v1.disable_eager_execution()

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

  # Splitting data
  X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=None, shuffle=True, stratify=Y)

  # Restore it
  classifier = SupervisedDBNClassification.load('model.pkl')
  # Test
  Y_pred = classifier.predict(X_test)
  
  target_names = ['Win', 'Loss']
  print(classification_report(Y_test, Y_pred, target_names=target_names))
  print(accuracy_score(Y_test, Y_pred))


dbn_siamese('training_2.csv')

