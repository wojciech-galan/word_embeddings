#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import constants
import pickle


def read(fname=constants.PROT_VEC_CSV):
    ret_dir = {}
    with open(fname) as f:
        for line in f:
            k, v = line.rstrip().strip('"').split(None, 1)
            v = np.array([float(x) for x in v.split()])
            ret_dir[k] = v
    return ret_dir


if __name__ == '__main__':
    prot_vecs = read()
    print(type(prot_vecs))
    with open(constants.PROT_VEC_PICKLE, 'wb') as outfile:
        pickle.dump(prot_vecs, outfile)