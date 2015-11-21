#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: prgrpt.py
# $Date: Sun Aug 17 23:25:20 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>


import time


class ProgressReporter(object):
    def __init__(self):
        self.start_time = time.time()

    def report(self, cnt):
        duration = time.time() - self.start_time
        speed = cnt / duration
        print '{} items/sec'.format(speed)


# vim: foldmethod=marker

