#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: plot_2d_distribution.py
# $Date: Sun Aug 17 15:13:54 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import argparse
import sys
import matplotlib.pyplot as plt
import numpy
from collections import Counter
import pandas
from IPython import embed


def do_main(csv_file, frame, column_0, column_1, save_to):

    print 'aggregating data ...'
    data_c0, data_c1 = frame[column_0], frame[column_1]
    cnt_c0, cnt_c1 = map(Counter, [data_c0, data_c1])

    nr_keys = len(cnt_c0) * len(cnt_c1)
    print '#keys: {}'.format(nr_keys)
    if len(cnt_c0) > 200 or len(cnt_c1) > 200 or nr_keys > 200 * 200:
        print 'too many keys for file `{}\' column `{},{}\': {}'.format(
                csv_file, column_0, column_1, nr_keys)
        return

    key2num = lambda counter: dict(map(
        lambda x: (x[1], x[0]), enumerate(counter.keys())))

    key2num_c0, key2num_c1 = map(key2num, [cnt_c0, cnt_c1])

    counts = Counter(zip(data_c0, data_c1))

    print 'plotting ...'
    keys, values = counts.keys(), counts.values()

    plt.figure(figsize=(8 * 2 * 2, 8 * 2 * 2))

    data = numpy.zeros(map(len, [cnt_c0, cnt_c1]))
    for (x, y), v in zip(keys, values):
        data[key2num_c0[x]][key2num_c1[y]] = v

#     embed()
#     print data
    print data.shape
    plt.imshow(data)
    plt.yticks(numpy.arange(len(cnt_c0)), cnt_c0.keys())
    plt.xticks(numpy.arange(len(cnt_c1)), cnt_c1.keys())

    plt.title('File: {}, column: {}-{}'.format(csv_file, column_0, column_1))

    plt.tight_layout()
    plt.savefig(save_to)

#     plt.show()

def main():
    print sys.argv
    if len(sys.argv) != 5:
        print 'Usage: {} <file> <column_0> <column_1> <save_to>'.format(
                sys.argv[0])
        sys.exit(1)

    csv_file, column_0, column_1, save_to = (
            sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])

    print 'reading file ...'
    frame = pandas.read_csv(csv_file, sep='\t', header=None)

    do_main(csv_file, frame, column_0, column_1, save_to)


if __name__ == '__main__':
    main()




# vim: foldmethod=marker

