#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from src.disorder_parser import *
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import LSTM


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
    pass


if __name__ == '__main__':
    X_train, Y_train = get_DM_data(open(os.path.join('..', "disorder", 'trainDM')).read())
    X_test, Y_test = get_DM_data(open(os.path.join('..', "disorder", 'testDM')).read())
    network(X_train, Y_train, X_test, Y_test)