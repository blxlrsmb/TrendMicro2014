#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: utils.py
# $Date: Sun Aug 17 20:19:19 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>


def one_hot(v, n):
    return [0] * v + [1] + [0] * (n - v - 1)


# vim: foldmethod=marker

