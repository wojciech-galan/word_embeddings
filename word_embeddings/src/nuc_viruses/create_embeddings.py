#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
from .constants import CONTAINER_PATH

class Sequence(object):

    def __init__(self, gi, embeddings, lineage, host_lineage):
        super().__init__()


def read_container(path=CONTAINER_PATH):
    with open(path, 'rb') as f:
        return pickle.load(f)

def get_sequences(conditions, container_path=CONTAINER_PATH):
    print (' and '.join(conditions))
    return {x.gi:Sequence() for x in read_container(container_path) if eval(' and '.join(conditions))}


if __name__ == '__main__':
    pass