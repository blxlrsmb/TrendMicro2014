#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: plot48.py
# $Date: Mon Aug 18 07:24:24 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import sys
import matplotlib.pyplot as plt

import seaborn
seaborn.set_context()
import numpy
from collections import Counter
import pandas
from IPython import embed
from plot import *


def read_csv(path):
    print path
    return pandas.read_csv(path, sep='\t', header=None)

def main():
    if len(sys.argv) != 4:
        print 'Usage: {} <csv_data_file> <web_category.tsv> <out>'.format(
            sys.argv[0])
        sys.exit(1)

    csv_file, web_category_path = sys.argv[1], sys.argv[2]

    data, cate = map(read_csv, [csv_file, web_category_path])

    num2type = dict(zip(cate[0], map(str, cate[1])))

    col4 = map(lambda x: num2type[x] if x in num2type else x, data[4])
    col8 = data[8]

    data, rownames, colnames = pair2data(col4, col8)

    new_data = []
    for row in data:
        a, b = 0.0, 0.0
        for i in range(len(row)):
            a += row[i] * colnames[i]
            b += row[i]
        new_data.append(a / b)
    print new_data

    print new_data
    print rownames

    ranges = numpy.arange(len(new_data))
    plt.figure(figsize=(20, 6))
    plt.bar(ranges, new_data)
    min_y, max_y = min(new_data), max(new_data)
    print min_y, max_y
    plt.hlines(min_y, ranges[0] - 10, ranges[-1] + 10, linestyles='dashed',
            colors='gray')
    plt.hlines(max_y, ranges[0] - 10, ranges[-1] + 10, linestyles='dashed',
            colors='gray')
    plt.xlim(ranges[0] - 0.3, ranges[-1] + 1 + 0.3)
    plt.xticks(ranges + 0.5, rownames)
    plt.title('Category Average Score')
    plt.xlabel('Category')
    plt.ylabel('Average Score')
    plt.tight_layout()
    plt.savefig(sys.argv[3])



if __name__ == '__main__':
    main()


# vim: foldmethod=marker

