#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: plot_column_distribution.py
# $Date: Sun Aug 17 14:18:23 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import argparse
import sys
import matplotlib.pyplot as plt
import numpy
from collections import Counter
import pandas


def main():
    if len(sys.argv) != 4:
        print 'Usage: {} <file> <column> <save_to>'.format(sys.argv[0])
        sys.exit(1)

    csv_file, column, save_to = sys.argv[1], int(sys.argv[2]), sys.argv[3]

    print 'reading file ...'
    frame = pandas.read_csv(csv_file, sep='\t', header=None)

    print 'aggregating data ...'
    counts = Counter(frame[column])

    print 'plotting ...'
    keys, values = counts.keys(), counts.values()

    print '#keys: {}'.format(len(keys))
    if len(keys) >= 200:
        print 'too many keys for file `{}\' column `{}\': {}'.format(
                csv_file, column, len(keys))
        sys.exit(1)

    plt.figure(figsize=(8 * 2 * 2, 6 * 2 * 2))
    plt.bar(range(len(keys)), values)
    plt.xticks(numpy.arange(len(keys)) + 0.5, keys)

    plt.title('File: {}, column: {}'.format(csv_file, column))

    plt.tight_layout()
    plt.savefig(save_to)

#     plt.show()


if __name__ == '__main__':
    main()




# vim: foldmethod=marker

