"""
Get metadata about an arbitrary number of random Wikipedia mainspace articles.
"""
import requests
import sys
import json

S = requests.Session()
RAND_URL = 'https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnlimit=500&rnnamespace=0'

def get_batch():
    r = S.get(url=RAND_URL)
    dat = r.json()
    # List of dictionaries, each having keys "id", "ns", and "title"
    pgs = dat['query']['random']
    return pgs
    
try:
    n = int(sys.argv[1])
except:
    print("USAGE: get_randos.py N")
    sys.exit(1)

acc = []

while len(acc) < n:
    acc += get_batch()
    print('.', end='')

# TODO: Consider filtering out dupes? This is unlikely to be a problem. Though, because of the
# way it's implemented, if we get any dupes, we'll get a lot...

out_fname = 'pages.json'
with open(out_fname, 'w') as f:
    json.dump(acc, f)
