#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: add_renewed_column.py
# $Date: Sun Aug 17 19:56:34 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>


import lib.data
from lib.config import config

import sys

def main():
    if len(sys.argv) != 4:
        print 'Usage: {} <input> <id_column> <output>'.format(
                sys.argv[0])
        sys.exit(1)

    input_path, id_column, output_path = sys.argv[1:]
    id_column = int(id_column)

    with open(output_path, 'w') as f:
        for row in lib.data.iter_rows(input_path):
            f.write('\t'.join(
                row + [str(config.is_renewed(row[id_column]))])
                + '\n')


if __name__ == '__main__':
    main()

# vim: foldmethod=marker
