import pandas as pd

fname = 'views.csv'

cols = ['title', *range(1, 13), 'total']
df_raw = pd.read_csv(fname, header=None, names=cols)

# Exclude any rows with any nans - indicating page didn't exist for all of 2021
df = df_raw.dropna()

# (Preliminary investigation suggests no cases where we have nans sandwiching a non-nan value - which would call into question our theory above. But haven't checked exhaustively.)
# Actually, hm, this gets 2 results for my 20k sample (non-nan for Jan, nan for Feb):
# df[~pd.isnull(df.loc[:,1]) & (pd.isnull(df.loc[:,2])) ]

# This gets 16 results for my 20k sample
# Most plausible explanation would seem to be the page was deleted, right?
"""
Examples:

https://en.wikipedia.org/wiki/Giorgi_Kakhiani
- created 07/30/2021
- draftified 08/01/2021
- recreated in mainspace 01/09/2022
So was only live in mainspace for about 24 hours. During that time it managed to get 65 views in July and 6 in August.

https://en.wikipedia.org/wiki/Thomas_Alsbury
- created as redirect Feb 2009
- made into a dab page Jul 10 2021
- no incoming links
- gets single digit views most months (even just 1 in Mar), but nan in June
- this confirms a redirect can get 0 views in a month

https://en.wikipedia.org/wiki/Thomas_Allen_(divine,_Thomas_Allen_(1608-1673)))
- interesting that this was even returned by random endpoint, since it's not supposed to give redirects. Possibly was not detected as such because it happened to have a speedy deletion tag on it?
- another case of a weird redirect with no incomings that generally gets single-digit views, and sometimes 0

Stephen Hogan
- created April 2021
- draftified May 2021
- recreated Aug 2021(?)
- got plenty of views April/May, then a two month gap, then plenty of views from Aug onward

Basically, it *seems* like all nans can be explained by one of the following:
    - the page didn't exist at the time
    - the page only existed as a redirect at the time (and an obscure one at that)
"""
def get_gaps(df):
    mask = None
    for month in range(2, 13):
        update = (~pd.isnull(df.loc[:,month-1])) & (pd.isnull(df.loc[:,month]))
        if mask is None:
            mask = update
        else:
            mask = mask | update
    return df[mask]
