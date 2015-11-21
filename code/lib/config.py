#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: config.py
# $Date: Sun Aug 17 23:23:43 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>


class Config(object):

    def __init__(self):
        self._unrenewed_ids = None
        self._renewed_ids = None
        self._is_renewed = None

    def unrenewed_ids(self):
        if self._unrenewed_ids is None:
            with open('ids/unrenewed-ids.list') as f:
                self._unrenewed_ids = [line.rstrip() for line in f]
        return self._unrenewed_ids

    def renewed_ids(self):
        if self._renewed_ids is None:
            with open('ids/renewed-ids.list') as f:
                self._renewed_ids = [line.rstrip() for line in f]
        return self._renewed_ids

    def has_renew_info(self, id):
        if self._is_renewed is None:
            self.is_renewed(id)
        return id in self._is_renewed

    def is_renewed(self, id):
        if self._is_renewed is None:
            renewed_ids = self.renewed_ids()
            unrenewed_ids = self.unrenewed_ids()
            self._is_renewed = dict(
                zip(renewed_ids, [1] * len(renewed_ids)) +
                zip(unrenewed_ids, [0] * len(unrenewed_ids)))

        if id in self._is_renewed:
            return self._is_renewed[id]
        return None


config = Config()

# vim: foldmethod=marker

