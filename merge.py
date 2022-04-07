"""
Merge csv with basic page metadata (as downloaded from Quarry) with one having
pageviews per page, as produced by get_views.py.
"""
import pandas as pd
import sys

qname = 'qgapped.csv'
qname = '30k_smallest_gaps.csv'
qname = '100k_smallest_gaps.csv'
qname = 'phaeg_gaps.csv'
qname = '600k.csv'
vname = 'views.csv'

qname = sys.argv[1]
vname = sys.argv[2]

def load_views():
    cols = ['page_title', *range(1, 13), 'total']
    df_raw = pd.read_csv(vname, header=None, names=cols)
    return df_raw

qf = pd.read_csv(qname)
vf = load_views()

assert len(qf) == len(vf), f"len(qf) = {len(qf)} != {len(vf)} = len(vf)"

df = qf.merge(vf, on='page_title')

df.to_csv('merged.csv', index=False)
