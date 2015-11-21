#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: plot_2d_web_all.py
# $Date: Sun Aug 17 15:30:53 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>


import os
import sys
import pandas
from collections import Counter
import multiprocessing
from multiprocessing import Pool

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



def main():
    if len(sys.argv) != 3:
        print 'Usage: {} <file> <save_dir>'.format(sys.argv[0])
        sys.exit(1)

    csv_file, save_dir = sys.argv[1], sys.argv[2]
    frame = pandas.read_csv(csv_file, sep='\t', header=None)
    counters = map(Counter, [frame[i] for i in range(len(frame.columns))])

    pool = Pool()

    permitted = [2, 4, 7, 8]
    for i in permitted:
        for j in permitted:
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

