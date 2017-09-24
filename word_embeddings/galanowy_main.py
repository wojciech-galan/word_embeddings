#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
from src.disorder_parser import *
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import TimeDistributed

# na razie na spokojnie bez maskowania

def get_DM_data(path):
    representations = []
    disorders = []
    for x in parse(path):
        l = list(x.get_representation_and_disorder())
        rep = [el[0] for el in l]
        dis = [el[1] for el in l]
        representations.append(rep)
        disorders.append(dis)
    return representations , disorders

def network(X_train, Y_train, X_test, Y_test, epochs):
    # first try
    # size of element of one sequence
    element_size = X_train[0][0].shape[0]
    X_train = [np.array(x).reshape((1, len(x), element_size)) for x in X_train]
    Y_train = [np.array(y).reshape((1, len(y), 1)) for y in Y_train]
    X_test = [np.array(x).reshape((1, len(x), element_size)) for x in X_test]
    Y_test = [np.array(y).reshape((1, len(y), 1)) for y in Y_test]
    print([x.shape for x in X_train])
    model = Sequential()
    model.add(LSTM(588, return_sequences=True, input_shape=(None, 100), batch_input_shape=(1, None, 100)))
    model.add(TimeDistributed(Dense(1)))
    # jednak jak mamy output jako liczby rzeczywiste (0, 0.333, 0.667, 1), to chyba trzeba loss=mean_squared_error
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    # train model
    for epoch in range(epochs):
        print('Epoka', epoch)
        for seq, label in zip(X_train, Y_train):
            print(seq.shape, label.shape)
            model.fit(seq, label, batch_size=1, epochs=1, shuffle=False)
    # evaluate
    for i in range(len(X_test)):
        result = model.predict(X_test[i], batch_size=1, verbose=0)
        print ('--------------------------------\nwyniczek')
        for x, y in zip(result[0], Y_test[i][0]):
            print(x[0], y[0])


if __name__ == '__main__':
    # z jednej sekwencji myślę, że trzeba będzie zrobić 3 w różnych ramkach (jeszcze nie zrobione)
    X_train, Y_train = get_DM_data(open(os.path.join("disorder", 'trainDM')).read())
    X_test, Y_test = get_DM_data(open(os.path.join("disorder", 'testDM')).read())
    network(X_train, Y_train, X_test, Y_test, epochs=1)