#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: plot-num.py
# $Date: Mon Aug 18 00:47:33 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import matplotlib.pyplot as plt
import numpy
import sys


def main():
    if len(sys.argv) != 4:
        print 'Usage: {} <input> <nr_bins> <output>'.format(sys.argv[0])
        sys.exit(1)

    input_path, nr_bins, output_path = sys.argv[1:]
    nr_bins = int(nr_bins)

    data = []
    with open(input_path) as f:
        for line in f:
            line = line.rstrip()
            if not line:
                continue
            line = line.split()
            if not line:
                continue

            data.extend(map(float, line))

    y, x = numpy.histogram(data, nr_bins)
    x = (numpy.array(list(x) + [0]) + numpy.asarray([0] + list(x)))[1:-1] * 0.5
    min_x, max_x = min(x), max(x)
    width = (max_x - min_x) / float(nr_bins) * 0.9
    plt.bar(x, y, width=width)
    plt.grid()
    plt.savefig(output_path)
    plt.show()


if __name__ == '__main__':
    main()

# vim: foldmethod=marker

