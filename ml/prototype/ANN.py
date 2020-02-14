import numpy as np
import tensorflow as tf
import math, sys
import logging
logging.basicConfig(level=logging.DEBUG)
import scipy.io as sio # The library to deal with .mat


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

raw_train_data = get_dataset('features.csv')
raw_test_data = get_dataset('eval.csv')


print(type(raw_test_data))

show_batch(raw_train_data)
show_batch(raw_test_data)

packed_train_data = raw_train_data.map(pack)
test_data = raw_test_data.map(pack)




model = tf.keras.Sequential([
  tf.keras.layers.Dense(75, activation='relu'),
  tf.keras.layers.Dense(50, activation='relu'),
  tf.keras.layers.Dense(25, activation='relu'),
  tf.keras.layers.Dense(1, activation='sigmoid'),
])


model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy'])

train_data = packed_train_data

#test_data = packed_test_data

model.fit(train_data, epochs=100)
test_loss, test_accuracy = model.evaluate(test_data)

print('\n\nTest Loss {}, Test Accuracy {}'.format(test_loss, test_accuracy))

predictions = model.predict(test_data)

# Show some results
for prediction, win in zip(predictions[:100], list(test_data)[0][1][:100]):
  print("Predicted Win: {:.2%}".format(prediction[0]),
        " | Actual outcome: ",
        ("WIN" if bool(win) else "LOSS"))


model.save('caterpillar.h5')
