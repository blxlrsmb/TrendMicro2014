#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: split_data.py
# $Date: Sun Aug 17 21:05:26 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import sys


def main():
    if len(sys.argv) != 5:
        print 'Usage: {} <input> <out1_ratio> <out1> <out2>'.format(
            sys.argv[0])
        sys.exit(1)

    input_path, ratio, out1, out2 = sys.argv[1:]
    ratio = float(ratio)

    with open(input_path) as fin:
        data = [line.rstrip() for line in fin]

    nr_out1 = int(len(data) * ratio)
    nr_out2 = len(data) - nr_out1

    def write_file(path, rows):
        with open(path, 'w') as fout:
            for row in rows:
                print >> fout, row

    write_file(out1, data[:nr_out1])
    write_file(out2, data[nr_out1:])


if __name__ == '__main__':
    main()

# vim: foldmethod=marker

