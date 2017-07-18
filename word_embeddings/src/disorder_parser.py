#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re


class Sequence(object):

    def __init__(self):
        super().__init__()


def parse(txt):
    sequences = []
    i = 0
    lines = []
    def parse_2nd_line(a_line):
        assert a_line.startswith('$')
        LAST_EMEMENT_RE =
        for element in a_line.split()[1:]:
            if element.startswith('#'):

    for line in txt.split(os.linesep):
        lines.append(line)
        if i%4 == 0:
            title = line[0][1:]
            sequences.append(Sequence())
        i += 1


if __name__ == '__main__':
    parse(open('../disorder/DM4229.db').read())