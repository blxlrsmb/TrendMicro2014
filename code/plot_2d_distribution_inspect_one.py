#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: plot_2d_distribution_inspect_one.py
# $Date: Sun Aug 17 20:04:21 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>


import os
import sys
import pandas
from collections import Counter
import multiprocessing
from multiprocessing import Pool
from plot_2d_distribution import do_main

def main():
    if len(sys.argv) != 4:
        print 'Usage: {} <file> <column> <save_dir>'.format(sys.argv[0])
        sys.exit(1)

    csv_file, column, save_dir = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    frame = pandas.read_csv(csv_file, sep='\t', header=None)
    counters = map(Counter, [frame[i] for i in range(len(frame.columns))])

    pool = Pool()

    i = column
    for j in range(len(counters)):
        nr_keys = len(counters[i]) * len(counters[j])
        if len(counters[i]) > 200 or len(counters[i]) > 200 or nr_keys > 200 * 200:
            print 'too many keys columns `{},{}\': {}'.format(
                i, j, nr_keys)
        else:
            print 'columns `{},{}\' passed'.format(i, j)
            pool.apply_async(do_main, [
                csv_file, frame, i, j, os.path.join(
                    save_dir, '{}-{}.png'.format(i, j))])

    pool.close()
    pool.join()
    pool.terminate()


if __name__ == '__main__':
    main()


# vim: foldmethod=marker

