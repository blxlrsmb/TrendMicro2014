#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: plot48_heatmap.py
# $Date: Mon Aug 18 07:41:38 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import sys
import matplotlib.pyplot as plt

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

    data = data.T
    plt.figure(figsize=(10 * 2, 4 * 2))
    plt.imshow(data)
    plt.yticks(range(data.shape[0]), colnames)
    plt.xticks(range(data.shape[1]), rownames)
    plt.xlabel('Score')
    plt.ylabel('Category Group')

#     plt.title('Category Average Score')
#     plt.xlabel('Category')
#     plt.ylabel('Average Score')
    plt.tight_layout()
    plt.savefig(sys.argv[3])



if __name__ == '__main__':
    main()


# vim: foldmethod=marker

