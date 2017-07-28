#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import abc
import pickle
import constants
from convert import convert

# + means disordered residue
# - means odrered residue
# X means no information
REPLACEMENT_DICT = {'O':'-', 'D':'+'}
DISORDER_VALUE_DICT = {'-':0, '+':1}
DISORDER_FORBIDDEN_VALUE = 'X'
REPRESENTATION_DICT = pickle.load(open(constants.PROT_VEC_PICKLE, 'rb'))

LAST_ELEMENT_RE = re.compile('(\d+)-(\d+)')
SEQ_RE = re.compile('>[^>]+')
NUMERIC_OR_COMMA_RE = re.compile('[\d,]+')
CASP_RE = re.compile('^PFRMAT	DR\s+^TARGET\s+(\S+)\s+((^.\s.\s\d+\s)+)END', re.MULTILINE)


class BaseSequence(abc.ABC):

    def __init__(self, title, seq, disorder, representation_dict=REPRESENTATION_DICT, word_size=3,
                 forbidden_value=DISORDER_FORBIDDEN_VALUE, value_dict=DISORDER_VALUE_DICT):
        assert len(seq) == len(disorder)
        super().__init__()
        self.title = title
        self.seq = seq
        self.disorder = disorder
        self.word_size = word_size
        self.__representation_dict = representation_dict
        self.__forbidden_value = forbidden_value
        self.__value_dict = value_dict

    # def __get_embeddings(self, frame):
    #     return convert(self.seq, pickle.load(open(constants.PROT_VEC_PICKLE, 'rb')), self.word_size, frame)

    def get_representation_and_disorder(self):
        """
        Generator that yields tuples (embeddings, value_for_disorder).
        :param frame:
        :return:
        """
        def transform_disorder_string_to_value(disorder_string):
            return sum(self.__value_dict[x] for x in disorder_string)/len(disorder_string)
        for x in range(0, len(self.seq)+1-self.word_size):
            if not self.__forbidden_value in self.disorder[x:x + self.word_size]:
                yield (self.__representation_dict[self.seq[x:x+self.word_size]],
                       transform_disorder_string_to_value(self.disorder[x:x+self.word_size]))

    @abc.abstractmethod
    def __repr__(self):
        pass


class Sequence(BaseSequence):
    """Represents protein sequences and their disordered regions from DM4229.db and SL477.db"""

    def __init__(self, title, sn, prot_size, total_dr, num_dr, size_dr, locations, seq, disorder):
        super().__init__(title, seq, disorder)
        self.sn = sn
        self.prot_size = prot_size
        self.total_dr = total_dr
        self.num_dr = num_dr
        self.size_dr = size_dr
        self.locations = locations

    def __repr__(self):
        return"Sequence ('%s', %s, %s, %s, %s, %s, %s, '%s', '%s')"%(self.title, self.sn, self.prot_size, self.total_dr,
                                                                self.num_dr, str(self.size_dr), str(self.locations),
                                                                self.seq, self.disorder)


def _parse_2nd_line(a_line, location_re=LAST_ELEMENT_RE, num_or_comma_re=NUMERIC_OR_COMMA_RE):
    """Helper for 'parse' function"""
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
    """Parser for DM4229.db and SL477.db files"""
    for seq in sequence_re.findall(txt):
        lines = [s for s in seq.split(os.linesep) if s.strip()]
        title_string = lines[0][1:]
        sn, prot_size, total_dr, num_dr, size_dr, locations = _parse_2nd_line(lines[1], location_re, num_or_comma_re)
        seq = lines[2]
        disorder = lines[3]
        assert len(seq) == len(disorder)
        yield Sequence(title_string, sn, prot_size, total_dr, num_dr, size_dr, locations, seq, disorder)


class CASPSequence(BaseSequence):
    """Represents protein sequences and their disordered regions from CASP competition"""

    def __init__(self, name, seq, disorder):
        super().__init__(name, seq, disorder)
        self.prot_size = len(seq)

    def __repr__(self):
        return "CASPSequence ('%s', '%s', '%s')" %(self.title, self.seq, self.disorder)


def parse_casp_directory(directory, re_whole_file=CASP_RE, replacement_dict=REPLACEMENT_DICT):
    ret_list = []
    for file in os.listdir(directory):
        ret_list.append(parse_casp_file(os.path.join(directory, file), re_whole_file, replacement_dict))
    return ret_list


def parse_casp_file(f_path, re_whole_file=CASP_RE, replacement_dict=REPLACEMENT_DICT):
    seq = []
    disorder = []
    with open(f_path) as f:
        content = f.read()
        match = re_whole_file.match(content)
        assert match
        # group nr 1 contains the protein name
        target_name = match.group(1)
        # group nr 2 contains all the interesting lines
        for line in match.group(2).strip().split('\n'):
            splitted = line.split()
            seq.append(splitted[0])
            disorder.append(splitted[1])
        disorder = [replacement_dict.get(c, DISORDER_FORBIDDEN_VALUE) for c in disorder]
    return CASPSequence(target_name, ''.join(seq), ''.join(disorder))


if __name__ == '__main__':
    for seq in parse_casp_directory('../disorder/casp9.DR_targets/'):
        #print (seq._BaseSequence__get_disorder_values(0))
        #print(seq._BaseSequence__get_disorder_values(1))
        print (seq.disorder)

    for seq in parse(open('../disorder/SL477.db').read()):
        print(seq)

    seq = CASPSequence('bla', 'AGATA', '---++')
    print (seq)
    for representation, disorder in seq.get_representation_and_disorder():
        print (representation)
        print (disorder)
        print ('__________________')