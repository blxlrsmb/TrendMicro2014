#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: data.py
# $Date: Mon Aug 18 00:06:39 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import csv
import codecs

class CsvDialect(object):
    delimiter = '\t'


def iter_rows(path, split=True):
    with open(path) as f:
        if split == True:
            for row in csv.reader(f, dialect=CsvDialect):
                yield row
        else:
            for line in f:
                yield line.rstrip()


def iter_filter(filter_func, iterator):
    for i in iterator:
        if filter_func(i):
            yield i


# vim: foldmethod=marker
