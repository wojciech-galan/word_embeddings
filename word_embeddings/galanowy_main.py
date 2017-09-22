#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
from src.disorder_parser import *
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


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

def network(X_train, Y_train, X_test, Y_test):
    # first try
    # size of element of one sequence
    element_size = X_train[0][0].shape[0]
    X_train = [np.array(x).reshape((1, len(x), element_size)) for x in X_train]
    Y_train = [np.array(y).reshape((1, len(y), 1)) for y in Y_train]
    print([x.shape for x in X_train])
    model = Sequential()
    model.add(LSTM(588, return_sequences=True, input_shape=(None, 100), batch_input_shape=(1, None, 100)))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    for seq, label in zip(X_train, Y_train):
        print(seq.shape, label.shape)
        model.fit(seq, label, batch_size=1, nb_epoch=1, shuffle=False)
        #model.reset_states()

if __name__ == '__main__':
    X_train, Y_train = get_DM_data(open(os.path.join("disorder", 'trainDM')).read())
    X_test, Y_test = get_DM_data(open(os.path.join("disorder", 'testDM')).read())
    network(X_train, Y_train, X_test, Y_test)