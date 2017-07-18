#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re

LAST_ELEMENT_RE = re.compile('(\d+)-(\d+)')
SEQ_RE = re.compile('>[^>]+')
NUMERIC_OR_COMMA_RE = re.compile('[\d,]+')


class Sequence(object):

    def __init__(self, title, sn, prot_size, total_dr, num_dr, size_dr, locations, seq, disorder):
        super().__init__()
        self.title = title
        self.sn = sn
        self.prot_size = prot_size
        self.total_dr = total_dr
        self.num_dr = num_dr
        self.size_dr = size_dr
        self.locations = locations
        self.seq = seq
        self.disorder = disorder

    def __repr__(self):
        return"Sequence ('%s', %s, %s, %s, %s, %s, %s, '%s', '%s')"%(self.title, self.sn, self.prot_size, self.total_dr,
                                                                self.num_dr, str(self.size_dr), str(self.locations),
                                                                self.seq, self.disorder)


def _parse_2nd_line(a_line, location_re=LAST_ELEMENT_RE, num_or_comma_re=NUMERIC_OR_COMMA_RE):
    assert a_line.startswith('$')
    elements = a_line.split()[1:]
    assert elements[0].startswith('sn') and elements[1].startswith('prot_size') and \
           elements[2].startswith('total_dr') and elements[3].startswith('num_dr') and \
           elements[4].startswith('size_dr')
    assert all([x.startswith('#') for x in elements[5:]])

    def get_val(string, pattern=num_or_comma_re):
        try:
            return pattern.findall(string)[0]
        except IndexError:# no element found
            return ''
    sn = int(get_val(elements[0]))
    prot_size = int(get_val(elements[1]))
    total_dr = int(get_val(elements[2]))
    num_dr = int(get_val(elements[3]))
    size_dr = [int(x) for x in get_val(elements[4]).split(',') if x]
    # location
    locations = []
    for element in elements[5:]:
        location = re.search(location_re, element).groups()
        locations.append((int(location[0]), int(location[1])))
    return sn, prot_size, total_dr, num_dr, size_dr, locations


def parse(txt, sequence_re=SEQ_RE, location_re=LAST_ELEMENT_RE, num_or_comma_re=NUMERIC_OR_COMMA_RE):
    for seq in sequence_re.findall(txt):
        lines = [s for s in seq.split(os.linesep) if s.strip()]
        title_string = lines[0][1:]
        sn, prot_size, total_dr, num_dr, size_dr, locations = _parse_2nd_line(lines[1], location_re, num_or_comma_re)
        seq = lines[2]
        disorder = lines[3]
        assert len(seq) == len(disorder)
        yield Sequence(title_string, sn, prot_size, total_dr, num_dr, size_dr, locations, seq, disorder)


if __name__ == '__main__':
    for seq in parse(open('../disorder/SL477.db').read()):
        print(seq)