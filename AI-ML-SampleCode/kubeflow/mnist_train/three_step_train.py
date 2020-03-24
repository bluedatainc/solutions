from datetime import datetime
import tensorflow as tf
import numpy as np
import os
import sys

model_file = str(sys.argv[1])
data_file = str(sys.argv[2])

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(512, activation=tf.nn.relu),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

print(model.summary())    

arr =  np.load(data_file)
X_train = arr['x_train']
y_train = arr['y_train']
X_test = arr['x_test']
y_test = arr['y_test']
#(X_train, y_train), (X_test, y_test)= tf.keras.datasets.mnist.load_data()
X_train, X_test = X_train / 255.0, X_test / 255.0

#     callbacks = [
#       tf.keras.callbacks.TensorBoard(log_dir='/home/joyvan' + '/logs/' + datetime.now().date().__str__()),
#       # Interrupt training if `val_loss` stops improving for over 2 epochs
#       tf.keras.callbacks.EarlyStopping(patience=2, monitor='val_loss'),
#     ]

model.fit(X_train, y_train, batch_size=32, epochs=5,
            validation_data=(X_test, y_test))

print("Done with fitting")
model.save(model_file)

print("Model saved at : " + model_file)
