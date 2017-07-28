#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
from . import constants


def convert(seq, representation_dictionary, wlen, start=0):
    """
    Transforms seq to sequence of vectors based on representation_dictionary. Assumes, that words in the sequence are
    not overlapping. To achieve the overlapping behaviour, repeat the conversion with different start values
    in range[0, wlen).
    :param seq: sequence to be processed
    :param representation_dictionary: dict {word:vec_of_nums(np.array)}
    :param wlen: word length
    :param start: first letter to be transformd to a word.
    :return:
    """
    assert start < len(seq)
    out_list = []
    for x in range(start, len(seq)-wlen+1, wlen):
        print(x, seq[x:x+wlen])
        out_list.append(representation_dictionary[seq[x:x+wlen]])
    return out_list

if __name__ == '__main__':
    print(convert('AGAR', pickle.load(open(constants.PROT_VEC_PICKLE, 'rb')), 3, 1))