#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: plot_feature_weight.py
# $Date: Mon Aug 18 07:54:45 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>


import sys
import matplotlib.pyplot as plt
import numpy
import seaborn
from collections import Counter

def main():
    if len(sys.argv) != 4:
        print 'Usage: {} <data_path> <top_n> <output>'.format(sys.argv[0])
        sys.exit(1)

    data_path, top_n, output_path = sys.argv[1:]
    top_n = int(top_n)

    with open(data_path) as f:
        data = map(
            lambda x: (x[0], float(x[1])),
            [line.rstrip().split('\t') for line in f])

    names, y = zip(*data[-top_n:])

    print names, y



if __name__ == '__main__':
    main()



# vim: foldmethod=marker
