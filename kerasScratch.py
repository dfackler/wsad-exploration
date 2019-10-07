from keras.models import Sequential
from keras.layers import Dense
import numpy as np

# create model
model = Sequential()

# add layers
model.add(Dense(units=64, activation='relu', input_dim=1))

# configure learning process
model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])

# create training data
x_train = np.arange(1, 100)
y_train = np.arange(101, 200)

# train model
model.fit(x_train, y_train, epochs=5, batch_size=32)

# evaluate model
loss_and_metrics = model.evaluate(x_test, y_test, batch_size=128)
