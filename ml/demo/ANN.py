import numpy as np
import tensorflow as tf
import math
import logging
logging.basicConfig(level=logging.DEBUG)
import scipy.io as sio # The library to deal with .mat


#Network parameters
n_hidden1 = 50
n_hidden2 = 25
n_input = 119
n_output = 1
#Learning parameters
learning_constant = 0.2
number_epochs = 1000
batch_size = 1000

def get_dataset(file_path, **kwargs):
  dataset = tf.data.experimental.make_csv_dataset(
      file_path,
      batch_size=100, # Artificially small to make examples easier to show.
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

raw_train_data = get_dataset('features.csv')
raw_test_data = get_dataset('eval.csv')

show_batch(raw_train_data)
show_batch(raw_test_data)

def pack(features, label):
  return tf.stack(list(features.values()), axis=-1), label

packed_train_data = raw_train_data.map(pack)
test_data = raw_test_data.map(pack)
#preprocessing_layer = tf.keras.layers.DenseFeatures(categorical_columns+numeric_columns)


model = tf.keras.Sequential([
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(1, activation='sigmoid'),
])


model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy'])

train_data = packed_train_data.shuffle(50)
#test_data = packed_test_data

model.fit(train_data, epochs=20)
test_loss, test_accuracy = model.evaluate(test_data)

print('\n\nTest Loss {}, Test Accuracy {}'.format(test_loss, test_accuracy))
