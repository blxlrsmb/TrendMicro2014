#!/usr/bin/env python2
# -*- coding: utf-8 -*- $File: feature.py
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

from utils import one_hot
from data import iter_rows
import copy
import operator
from prgrpt import ProgressReporter
from IPython import embed
import math

from virus_name_feature_data import virus_names

class VirusNameFeature(object):

    def __init__(self, column, num):
        self.column = column
        self.virus_names = map(operator.itemgetter(0), virus_names[:num])

        self.str2int = dict(map(
            lambda x: (x[1], x[0]), enumerate(self.virus_names)))

        self.data = [0] * len(self.virus_names)

    def update(self, row):
        s = row[self.column]
        for line in s.split(','):
            line = line.split(':')
            v = line[0]
            if v in self.str2int:
                self.data[self.str2int[v]] += 1

    def extract(self):
        return self.data
        #return one_hot(
        #        max(enumerate(self.data), key=operator.itemgetter(1))[0],
        #        len(self.data))

    def nr_features(self):
        return len(self.virus_names)

    def description(self):
        return [x + '-col-{}'.format(self.column) for x in self.virus_names]


class ProductIdFeature(object):

    product_ids = [i.split('\t')[0] for i in '''111	PCC14
125	PCC14
126	PCC15
144	IMSS7 Solaris
147	PCC16
148	PCC16
149	PCC16
1785	1785
201	TIS 17
202	TIS 17
221	TIS 17
230	IMSVA
23	OFCN35 NT
243	OSCE
451	WFBS 6
452	SMARTSURFING MAC
458	Housecall 7
459	Housecall Mac
499	Housecall 7
461	OSCE 10
463	TMSSS
468	WFBS_SVC_30
47	PCC9
493	MINITDA
495	Housecall 7
500	BROWSERGUARD
504	Housecall
510	iTIS 1-6
59	PCC10
604	HES SCANNER
63	IMSS
6BD	6BD
825753	825753
83	PCC11
96	PCC12
c12t1200v1	Vizor 1.0
c12t1200v2	TMS 2
c16t1600v1	WFBS 7
c16t1600v1.0.0l128p5889r4o1	WFBS 7
c17t170	TITANIUM 7.0
c17t1700v3	TITANIUM 3.0
c17t1700v5	TITANIUM 5.0
c17t1700v6	TITANIUM 6.0
c17t1700v7	TITANIUM 7.0
c17t1700v8	TITANIUM 8.0
TE80	TITANIUM 8.0
c22t2200v8	Deep Security 8.0
641	OSCE 11'''.split('\n')]

    def __init__(self, column):
        self.column = column
        self.str2int = dict(map(
            lambda x: (x[1], x[0]), enumerate(self.product_ids)))

        self.data = [0] * len(self.product_ids)

    def update(self, row):
        self.data[self.str2int[row[self.column]]] += 1

    def extract(self):
        return self.data
        #return one_hot(
        #        max(enumerate(self.data), key=operator.itemgetter(1))[0],
        #        len(self.data))

    def nr_features(self):
        return len(self.product_ids)

    def description(self):
        return self.product_ids


class VirusTypeFeature(object):

    virus_types = [0x59, 0x48, 0x30, 0x31, 0x43, 0x56, 0x00]

    def __init__(self, column):
        self.column = column
        self.str2int = dict(map(
            lambda x: (x[1], x[0]), enumerate(self.virus_types)))

        self.data = [0] * len(self.virus_types)

    def update(self, row):
        s = row[self.column]
        for line in s.split(','):
            line = line.split(':')
            v = int(line[6])
            if v in self.str2int:
                self.data[self.str2int[v]] += 1

    def extract(self):
        return self.data
        #return one_hot(
        #        max(enumerate(self.data), key=operator.itemgetter(1))[0],
        #        len(self.data))

    def nr_features(self):
        return len(self.virus_types)

    def description(self):
        return [str(x) + '-col-{}'.format(self.column) for x in self.virus_types]


class FeatureProxyMixin(object):

    def __init__(self, feature):
        self.feature = feature

    def update(self, row):
        self.feature.update(row)

    def extract(self):
        return self.feature.extract()

    def nr_features(self):
        return self.feature.nr_features()

    def description(self):
        return self.feature.description()


class CountryCodeFeature(object):

    country_codes = """
- # AD AE AF AI AL AM AP AR AS AT AU AW BA BD BE BG BH BM BN BO BQ BR BS BT BW
  BY BZ CA CH CL CN CO CR CU CW CY CZ DE DJ DK DM DO DZ EC EE EG ES EU FI FJ FM
  FO FR GB GE GG GI GL GR GT GU GY HK HN HR HT HU ID IE IL IM IN IQ IR IS IT JE
  JM JO JP KE KH KR KW KY KZ LA LB LI LK LT LU LV LY MA MD ME MG MK MM MN MO MP
  MT MU MV MX MY MZ NC NI NL NO NP NZ OM PA PE PG PH PK PL PLAE PR PT PY QA
  reserved RO RS RU SA SB SD SE SG SI SK SM SO SV SY TH TJ TN TR TT TW TZ UA UG
  US UY UZ VA VE VG VI VN VU WF WS YE ZA ZM ZW ZZ BB KG NG ET AG KG PS SR GH
         """.split()

    def __init__(self, column):
        self.column = column
        self.str2int = dict(map(
            lambda x: (x[1], x[0]), enumerate(self.country_codes)))

        self.data = [0] * len(self.country_codes)
        self.tot = 0

    def update(self, row):
        self.tot += 1
        code = row[self.column]
        if code not in self.str2int:
            print code
            return
        self.data[self.str2int[code]] += 1

    def extract(self):
        return map(lambda x: x * 1.0 / self.tot if self.tot else 0, self.data)
        return self.data
        return one_hot(
                max(enumerate(self.data), key=operator.itemgetter(1))[0],
                len(self.data))

    def nr_features(self):
        return len(self.country_codes)

    def description(self):
        return [x + '-col-{}'.format(self.column) for x in self.country_codes]


class TotalNumberRecordsFeature(object):
    def __init__(self):
        self.tot = 0

    def update(self, row):
        self.tot += 1

    def extract(self):
        return [self.tot]

    def nr_features(self):
        return 1

    def description(self):
        return ["Total number of records of this user"]

class TypeOfScoreFeature(object):
    def __init__(self):
        self.ret = [0 for _ in range(3)]
    def update(self, row):
        sc = int(row[8])
        if sc == 81:
            self.ret[0] += 1
        elif sc == 71:
            self.ret[1] += 1
        else:
            self.ret[2] += 1
    def extract(self):
        self.ret.extend(map(lambda x: x * 1.0 / sum(self.ret), self.ret))
        return self.ret
    def nr_features(self):
        return 6

    def description(self):
        ret = ['typescore{0}'.format(k) for k in range(3)]
        ret.extend(['typescoreavgcnt{0}'.format(k) for k in range(3)])
        return ret

class CategoryFeature(object):
    category_data = """1	Adult	Adult/Mature Content
3	Adult	Pornography
4	Adult	Sex Education
5	Adult	Intimate Apparel/Swimsuit
6	Adult	Nudity
8	Adult	Alcohol/Tobacco
9	Adult	Illegal/Questionable
10	Adult	Tasteless
11	Adult	Gambling
14	Adult	Violence/Hate/Racism
15	Adult	Weapons
16	Adult	Abortion
18	Lifestyle	Recreation/Hobbies
20	Lifestyle	Arts/Entertainment
21	Business	Business/Economy
22	Lifestyle	Cult/Occult
23	Network Bandwidth	Internet Radio and TV
24	Communications and Search	Internet Telephony
25	Adult	Illegal Drugs
26	Adult	Marijuana
27	General	Education
29	Lifestyle	Cultural Institutions
30	Lifestyle	Activist Groups
31	Business	Financial Services
32	Business	Brokerage/Trading
33	Lifestyle	Games
34	General	Government/Legal
35	General	Military
36	General	Political/Activist Groups
37	General	Health
38	General	Computers/Internet
39	Internet Security	Proxy Avoidance
40	Communications and Search	Search Engines/Portals
41	Communications and Search	Infrastructure
42	Communications and Search	Blogs/Web Communications
43	Network Bandwidth	Photo Searches
44	Lifestyle	Alternative Journals
45	Business	Job Search/Careers
46	General	News/Media
47	Lifestyle	Personals/Dating
48	General	Translators/circumvent filtering
49	General	Reference
50	Communications and Search	Social Networking
51	Communications and Search	Chat/Instant Messaging
52	Communications and Search	Email
53	Communications and Search	Newsgroups
54	Lifestyle	Religion
55	Lifestyle	Personal Websites
56	Network Bandwidth	Personal Network Storage/File Download Servers
57	Network Bandwidth	Peer-to-Peer
58	Business	Shopping
59	Business	Auctions
60	Business	Real Estate
61	Lifestyle	Society/Lifestyle
62	Lifestyle	Gay/Lesbian
63	Lifestyle	Sport Hunting and Gun Clubs
64	Lifestyle	Restaurants/Dining/Food
65	Lifestyle	Sports
66	Lifestyle	Travel
67	General	Vehicles
68	Lifestyle	Humor/Jokes
69	Network Bandwidth	Streaming Media/MP3
70	Network Bandwidth	Ringtones/Mobile Phone Downloads
71	Network Bandwidth	Software Downloads
72	Network Bandwidth	Pay to Surf
73	Internet Security	Potentially Malicious Software
74	Internet Security	Spyware
75	Internet Security	Phishing
76	Internet Security	Spam
77	Internet Security	Adware
78	Internet Security	Virus Accomplice
79	Internet Security	Disease Vector
80	Internet Security	Cookies
81	Internet Security	Dialers
82	Internet Security	Hacking
83	Internet Security	Joke Program
84	Internet Security	Password Cracking Apps
85	Internet Security	Remote Access Program
86	Internet Security	Made for AdSense sites (MFA)
87	Lifestyle	For Kids
88	Internet Security	Web Advertisement
89	Communications and Search	Web Hosting
90	General	No Category
91	NULL	Unknown"""

    def __init__(self, column):
        self.column = column
        conf = [line.rstrip().split('\t')
                for line in self.category_data.split('\n')]
        num2groupname = dict([(int(line[0]), line[1]) for line in conf])
        self.groupnames = list(set(num2groupname.values()))
        groupname2fid = dict([(x[1], x[0])
            for x in enumerate(self.groupnames)])

        self.num2fid = dict([
            (num, groupname2fid[num2groupname[num]])
            for num in num2groupname.keys()])

        self.data = [0] * len(self.groupnames)
        self.tot = 0

    def update(self, row):
        self.tot += 1
        i = int(row[self.column])
        if i not in self.num2fid:
            return
        i = self.num2fid[i]
        self.data[i] += 1

    def extract(self):
        return map(lambda x: x * 1.0 / self.tot, self.data)
        return self.data
        return map(lambda x: math.log(1 + x) if x > 0 else 0, self.data)
        return one_hot(
                max(enumerate(self.data), key=operator.itemgetter(1))[0],
                len(self.data))

    def nr_features(self):
        return len(self.data)

    def description(self):
        return map(lambda x: 'log-' + x, self.groupnames)


class ScoreFeature(object):

    def __init__(self, column):
        self.column = column
        self.sx, self.sx2 = 0, 0
        self.cnt = 0

    def update(self, row):
        v = int(row[self.column])
        self.sx += v
        self.sx2 += v * v
        self.cnt += 1

    def extract(self):
        if self.cnt:
            ave = self.sx / float(self.cnt)
            std = math.sqrt((self.sx2 / float(self.cnt) - ave**2) / self.cnt)
            return [ave] #, std]
        else:
            return [0.0]

    def nr_features(self):
        return 1

    def description(self):
        return ['score-ave']


class FeatureProxyMixin(object):

    def __init__(self, feature):
        self.feature = feature

    def update(self, row):
        self.feature.update(row)

    def extract(self):
        return self.feature.extract()

    def nr_features(self):
        return self.feature.nr_features()

    def description(self):
        return self.feature.description()

from datetime import datetime
class ActiveDaysFeature(object):
    def __init__(self):
        self.days = set()
    def update(self, row):
        time = row[0]
        time = datetime.fromtimestamp(float(time))
        self.days.add((time.month, time.day))

    def extract(self):
        return [len(self.days)]

    def nr_features(self):
        return 1
    def description(self):
        return ["active days"]

class VisitForeignFeature(object):
    def __init__(self):
        self.tot = 0
        self.realtot = 0
    def update(self, row):
        self.tot += row[2] == row[7]
        self.realtot += 1

    def extract(self):
        return [self.tot * 1.0 / self.realtot]

    def nr_features(self):
        return 1
    def description(self):
        return ["visitforeignwebsite"]

ZONEFILE = open('timezone.tsv')
ZONE = {}
for line in ZONEFILE:
    line = line.strip().split('\t')
    ZONE[line[0].lower()] = int(line[1]) / 100
class ActiveHourFeature(object):
    def __init__(self):
        self.slots = [0 for _ in range(6)]
    def update(self, row):
        time = row[0]
        time = datetime.fromtimestamp(float(time)).hour
        country = row[2].lower()
        if country in ZONE:
            time += ZONE[country]
            time = time / 4 % 6
            self.slots[time] += 1
    def extract(self):
        return map(lambda x: x * 1.0 / sum(self.slots), self.slots)

    def nr_features(self):
        return len(self.slots)
    def description(self):
        return ["activehour-{0}".format(i) for i in range(len(self.slots))]


class LogarithmFeatureWrapper(FeatureProxyMixin):
    def extract(self):
        return [math.log(1 + x) for x in self.feature.extract()]

    def description(self):
        return ['log-' + desc for desc in self.feature.description()]


class FeaturePool(object):
    def __init__(self, features_by_set_id):
        '''
        :param features_by_set_id: a dict feature_set_id -> features
        '''
        self.features_by_set_id = features_by_set_id
        self.features = sum(self.features_by_set_id.values(), [])

    def update(self, row, feature_set_id):
        for feature in self.features_by_set_id[feature_set_id]:
            try:
                feature.update(row)
            except Exception as e:
                print e

    def extract(self):
        vec = []
        for feat in self.features:
            try:
                vec.extend(feat.extract())
            except:
                vec.extend([0] * feat.nr_features())

        return vec

        return sum([feat.extract() for feat in self.features], [])

    def nr_features(self):
        return sum(feat.nr_features() for feat in self.features)

    def description(self):
        for feat in self.features:
            assert len(feat.description()) == feat.nr_features()

        return sum([feat.description() for feat in self.features], [])


class FeatureExtractor(object):
    def __init__(self, feat_pool, id_column, targetor, inlier,
            base_index=1, verbose=1):
        self.feat_pool = feat_pool
        self.id_column = id_column
        self.targetor = targetor
        self.inlier = inlier
        self.base_index = base_index

        self.instances = dict()


    def write_description(self, fpath):
        descs = self.feat_pool.description()
        assert len(descs) == self.feat_pool.nr_features()
        with open(fpath, 'w') as f:
            for i in range(len(descs)):
                print >> f, self.base_index + i, descs[i]

    def update(self, row_iterator, feat_set_id):
        rpt = ProgressReporter()
        for i, row in enumerate(row_iterator):
            if i % 100000 == 0:
                rpt.report(i)
            id = row[self.id_column]
            if not self.inlier(id):
                continue
            if id not in self.instances:
                self.instances[id] = copy.deepcopy(self.feat_pool)

            self.instances[id].update(row, feat_set_id)

    def write_instances(self, path):
        with open(path, 'w') as fout:
            for id, fp in self.instances.iteritems():
                y = self.targetor(id)
                x = []
                x = fp.extract()
                print >> fout, y, " ".join(
                    "{}:{}".format(self.base_index + k, v) for k, v in enumerate(x) if v != 0)

    def write_instance_ids(self, path):
        with open(path, 'w') as fout:
            for id in self.instances.iterkeys():
                print >> fout, id

# vim: foldmethod=marker
