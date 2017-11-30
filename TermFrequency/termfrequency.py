#!/usr/bin/env python

"""termfrequency.py:
This script determines the highest term frequency of each word in a list from a given set of files.

"""

__author__ = "Carrie L Rule"

import os
import re
import string
import sys
import logging
import argparse
from collections import Counter
from os.path import isfile, join
from os import listdir

# set up regex for removing punctuation
exclude = set(string.punctuation)
regex = re.compile('[%s]' % re.escape(string.punctuation))


# set up logger so info is written to a file instead of console
logging.getLogger().setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)-30s - %(levelname)-8s\n%(message)s')
fh = logging.FileHandler('log.txt')
fh.setFormatter(formatter)
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
logging.getLogger().addHandler(fh)
logging.getLogger().addHandler(ch)
logger = logging.getLogger(__name__)


def input_file_list(the_input=None):
    if the_input is None:
        the_input = input("Input path to directory containing files or path to files separated by a space:\n")
    if os.path.isdir(the_input):
        file_list = [join(the_input, f) for f in listdir(the_input) if isfile(join(the_input, f))]
    else:
        file_list = [f for f in the_input.split() if isfile(f)]
    if not file_list:
        with open('out.txt', 'w') as outfile:
            outfile.write('No files to search were given.')
        logger.info('No files to search were found.')
        sys.exit()
    else:
        logger.info('Files that will be searched:\n'+'\n'.join(file_list))
    return file_list


def input_word_list(string_of_words=None):
    if string_of_words is None:
        string_of_words = input("Input word(s) separated by space:\n")
    word_list = ''.join(regex.sub('', word) for word in string_of_words.lower())
    if not word_list:
        with open('out.txt', 'w') as outfile:
            outfile.write('No words to search for were given.')
        logger.info('No words to search for were given.')
        sys.exit()
    else:
        logger.info('Searching for words:\n' + '\n'.join(word_list.split()))
    return word_list


def create_term_frequency_dict(file_list, word_list):
    created_term_frequency_dict = {}
    for filename in file_list:
        file = open(filename, 'r')
        file_text = file.read()
        file_word_list = regex.sub('', file_text.lower()).split()
        num_words_in_file = len(file_word_list)
        word_count_dict = Counter(file_word_list)
        for word in word_list.split():
            created_term_frequency_dict[(word, filename.split('\\')[-1])] = \
                float(word_count_dict[word]/num_words_in_file)
        file.close()
    return created_term_frequency_dict


def find_max_term_frequency(word, term_frequency_dict):
    keys_for_word = list(k for k in term_frequency_dict if k[0] == word)
    max_key = keys_for_word[0]
    for key in keys_for_word:
        if term_frequency_dict[key] > term_frequency_dict[max_key]:
            max_key = key
    if term_frequency_dict[max_key] == 0.0:
        return None, None
    else:
        return max_key


def get_max_term_frequency_lists(word_list, term_frequency_dict):
    max_term_frequency_list_return = []
    if bool(term_frequency_dict):
        for word in word_list.split():
            max_key = find_max_term_frequency(word, term_frequency_dict)
            if max_key == (None, None):
                max_term_frequency_list_return.append((word, None, None))
            else:
                max_term_frequency_list_return.append((word, max_key[1], round(term_frequency_dict[max_key], 5)))
    return max_term_frequency_list_return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?')
    args = parser.parse_args()

    try:
        script_file = open(args.filename, 'r')
        files = input_file_list(script_file.readline().strip())
        words = input_word_list(script_file.readline().strip())
        script_file.close()
    except(FileNotFoundError, IOError, TypeError):
        files = input_file_list()
        words = input_word_list()

    term_frequency_dictionary = create_term_frequency_dict(files, words)
    max_term_frequencies = get_max_term_frequency_lists(words, term_frequency_dictionary)
    with open('out.txt', 'w') as outfile:
        for item in max_term_frequencies:
            if item[1] is None:
                outfile.write('The word "{0}" was not found in any document provided\n'.format(item[0]))
            else:
                outfile.write('The word "{0}" has the highest term frequency in the '
                              'document "{1}" of value {2}.\n'.format(item[0], item[1], item[2]))
