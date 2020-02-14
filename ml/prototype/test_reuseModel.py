import numpy as np
import tensorflow as tf
import math, sys
import logging
logging.basicConfig(level=logging.DEBUG)
import scipy.io as sio # The library to deal with .mat

#Loads module and evaluates pieces onto it
class evaluatePositions():
    def pack(self, features, label):
        return tf.stack(list(features.values()), axis=-1), label

    def get_dataset(self, file_path, **kwargs):
        dataset = tf.data.experimental.make_csv_dataset(
            file_path,
            batch_size=100, # Artificially small to make examples easier to show.
            label_name='Win',
            na_value="?",
            num_epochs=1,
            ignore_errors=True, 
            **kwargs)
        return dataset

    def run(self):
        new_model = tf.keras.models.load_model('/home/ubuntu/Documents/Shogi-DISS/src/ml/prototype/caterpillar.h5')
        new_model.summary()

        move_data = self.get_dataset('/home/ubuntu/Documents/Shogi-DISS/src/ml/prototype/moveposition.csv')
        move_data_packed = move_data.map(self.pack)
        predictions = new_model.predict(move_data_packed)

        index = 0
        best_score = 0
        best_solution = 0
        for prediction, win in zip(predictions, list(move_data)[0][1]):

            print("Predicted Win: {:.2%}".format(prediction[0]))
            if (prediction[0] > best_score):
                best_solution = index
                best_score = prediction[0]
            index += 1 
        
        return (best_solution)
        

#print(evaluatePositions().run())

