#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: gen_instances.py
# $Date: Mon Aug 18 03:56:25 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import argparse

from lib.data import *
from lib.config import config
from lib.feature import *


def fp_factory():
    return FeaturePool(dict(
        web2=[
            LogarithmFeatureWrapper(CountryCodeFeature(2)),
            LogarithmFeatureWrapper(CountryCodeFeature(7)),
            ScoreFeature(8),
            CategoryFeature(4),
            TotalNumberRecordsFeature(),
            ActiveDaysFeature(),
            VisitForeignFeature(),
            ActiveHourFeature(),
            ],
        det1=[
            VirusNameFeature(14, 100),
            VirusTypeFeature(14),
            ]))


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--web2', help='web2 file')
    parser.add_argument('--det1', help='det1 file')
    parser.add_argument('--inst-id', help='instance id file', required=True)
    parser.add_argument('--desc', help='output description file', required=True)
    parser.add_argument('--output', help='output instance file', required=True)

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    fp = fp_factory()

    feat_ext = FeatureExtractor(fp, -1,
            config.is_renewed, config.has_renew_info)
    feat_ext.write_description(args.desc)

    if args.web2:
        feat_ext.update(iter_rows(args.web2), 'web2')
    if args.det1:
        feat_ext.update(iter_rows(args.det1), 'det1')
    feat_ext.write_instances(args.output)
    feat_ext.write_instance_ids(args.inst_id)


if __name__ == '__main__':
    main()

# vim: foldmethod=marker
