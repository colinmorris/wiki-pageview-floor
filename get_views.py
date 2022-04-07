"""
Given the filename of a csv file with article metadata, write an augmented csv, views.csv,
with columns having monthly pageviews for 2021. Uses the Wikimedia pageview API, by way
of the mwviews wrapper.
"""
import json
import csv
import datetime
import time
import sys

import pandas as pd
from mwviews.api import PageviewsClient

def get_monthly_table(client, titles):
    """Return a dict mapping titles to lists of length 12, of ordered monthly view counts.
    """
    YR = 2021
    START = datetime.date(2021, 1, 1)
    END = datetime.date(2021, 12, 31)
    # Dictionary mapping date objects to dictionaries mapping titles to monthly counts.
    views = client.article_views('en.wikipedia', titles, granularity='monthly', start=START, end=END, agent='user')
    # For some reason mwviews returns dicts keyed by datetimes, rather than just dates.
    months = [datetime.datetime(YR, monthno, 1) for monthno in range(1, 13)]
    return { 
            title :
            [ views[month][munge_title(title)] for month in months ]
            for title in titles
    }

def munge_title(title):
    """Munging to match that done by the mwviews api before passing title to API
    (the results returned by mwviews use the munged titles rather than the versions
    passed to it)
    """
    #return requests.utils.quote(title.replace(' ', '_'), safe='')
    # Bleh, actually, more complicated. The above is what they pass to the API.
    # What they return to us is just *partially* munged.
    return title.replace(' ', '_')

def write_table_to_csv(table, fname):
    with open(fname, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        for title, views in table.items():
            # Also add a final total column
            row = [title, *views, sum([(v or 0) for v in views])]
            writer.writerow(row)

PGS_FNAME = 'pages.json'
def load_pagenames_from_json():
    with open(PGS_FNAME) as f:
        pgs = json.load(f)

    pagenames_a = [d['title'] for d in pgs]
    # Dedupe, just to be safe
    pagenames = list(set(pagenames_a))
    delta = len(pagenames_a) - len(pagenames)
    if delta > 0:
        print("Filtered out {} duplicate pages.".format(delta))

QUARRY_FNAME = 'quarry.csv'
QUARRY_FNAME = '30k_smallest_gaps.csv'
QUARRY_FNAME = '70k_smallest_gaps.csv'
QUARRY_FNAME = 'phaeg_gaps.csv'
QUARRY_FNAME = '600k.csv'
def load_pagenames_from_quarry_csv(fname):
    df = pd.read_csv(fname)
    return [str(title) for title in set(df.page_title)]
    

AGENT = '[[User: Colin M]] pageview floor analysis'
p = PageviewsClient(user_agent=AGENT)

fname = sys.argv[1]
pagenames = load_pagenames_from_quarry_csv(fname)


t0 = time.time()
dat = get_monthly_table(p, pagenames)
t1 = time.time()
print(f"Grabbed data for {len(pagenames)} pages in {t1-t0:.2f} seconds.")

write_table_to_csv(dat, 'views.csv')
