#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: plot.py
# $Date: Mon Aug 18 07:35:00 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import numpy
import matplotlib.pyplot as plt
from collections import Counter
from IPython import embed

def pair2data(data_c0, data_c1):

    data_c0, data_c1 = map(lambda d: filter(
        lambda x: str(x) != 'nan', d), [data_c0, data_c1])
    cnt_c0, cnt_c1 = map(Counter, [data_c0, data_c1])

    data = numpy.zeros(map(len, [cnt_c0, cnt_c1]))

    key2num = lambda counter: dict(map(
        lambda x: (x[1], x[0]), enumerate(counter.keys())))

    key2num_c0, key2num_c1 = map(key2num, [cnt_c0, cnt_c1])
#     embed()

    counts = Counter(zip(data_c0, data_c1))
    keys, values = counts.keys(), counts.values()

    for (x, y), v in zip(keys, values):
        data[key2num_c0[x]][key2num_c1[y]] = v

    return data, key2num_c0.keys(), key2num_c1.keys()


def plot_2d(data, rownames, colnames, save_to=None, show=False):
    data = numpy.asarray(data)

#     plt.figure(figsize=(32, 32))
    plt.imshow(data)
    plt.yticks(range(data.shape[0]), rownames)
    plt.xticks(range(data.shape[1]), colnames)

    plt.title('column: {}-{}'.format(*data.shape))

    plt.tight_layout()
    if save_to:
        plt.savefig(save_to)
    if show:
        plt.show()


def main():
    pass


if __name__ == '__main__':
    main()

# vim: foldmethod=marker

