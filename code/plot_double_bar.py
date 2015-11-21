#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: plot_double_bar.py
# $Date: Mon Aug 18 03:24:19 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

from sklearn.datasets import load_svmlight_file
import matplotlib.pyplot as plt
import numpy
import sys
from IPython import embed


def process_data(X, y, column, nr_bins):
    x = X[:,column].toarray().T[0]
    min_x, max_x = min(x), max(x)
    y = y[x != 0]
    x = x[x != 0]

    yp, p = numpy.histogram(x, nr_bins)
#     p = (numpy.array(list(p) + [0]) + numpy.asarray([0] + list(p)))[1:-1] * 0.5
    width = (max_x - min_x) / float(nr_bins) * 0.6

    y0, x0 = numpy.histogram(x[y == 0], p)
    y1, x1 = numpy.histogram(x[y == 1], p)
    p = (numpy.array(list(p) + [0]) + numpy.asarray([0] + list(p)))[1:-1] * 0.5

    return p, y0, y1, width


def main():
    if len(sys.argv) != 6:
        print 'Usage: {} <svm_file> <desc> <column> <nr_bins> <output>'.format(sys.argv[0])
        sys.exit(1)

    input_path, desc_path, column, nr_bins, output_path = sys.argv[1:]
    column, nr_bins = map(int, [column, nr_bins])

    with open(desc_path) as f:
        descs = [" ".join(line.rstrip().split()[1:]) for line in f]

    X, y = load_svmlight_file(input_path)

    x0, y0, y1, width = process_data(X, y, column, nr_bins)

    nr_items = sum(y0) + sum(y1)
    if nr_items < 100:
        print 'to few data for column {}: {}, abort.'.format(
            column, nr_items)
        return
    ff = open('/tmp/{0}'.format(descs[column]), 'w')
    print >> ff, x0, '\n', y0, '\n', y1
    ff.close()


    plt.bar(x0 + width * 0.3, y0, width=width, label='un-renewed', color='#55DD55')
    plt.bar(x0, y1, width=width, label='renewed', color='#5555DD')
    plt.title('distribution of {} on renewal'.format(descs[column]))
    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.savefig(output_path)
#     plt.show()


if __name__ == '__main__':
    main()


# vim: foldmethod=marker

