"""
Given a csv file with data about articles with a contiguous range of page_random values (quarry.csv),
write an updated csv file with a 'gap' column having the random gap.

(This is sort of a deprecated approach. Getting random gap values directly from quarry is simpler.)
"""
import pandas as pd

fname = 'quarry.csv'
df = pd.read_csv(fname)

gaps = []
prev_random = None
for _, row in df.iterrows():
    if prev_random is None:
        if row['pp_propname'] != 'disambiguation':
            prev_random = row['page_random']
        gaps.append(None)
        continue
    if row.pp_propname == 'disambiguation':
        # Gaps not meaningful for dab pages
        gaps.append(None)
        continue
    # The gap that we want to associate with each page is the distance between
    # its page_random value and the next-smallest value among non-dab pages.
    # (Recall how Special:Random works: select a random float in [0,1] and choose
    # the page with the next-highest page_random value.)
    gap = row.page_random - prev_random
    gaps.append(gap)
    prev_random = row.page_random

df['gap'] = gaps

df.to_csv('qgapped.csv', index=False)
