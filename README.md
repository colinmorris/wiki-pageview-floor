Trying to find and analyse the least viewed articles on English Wikipedia. Intend to turn this into a blog post at some point.

## Data pipeline

In the course of this investigation, I looked at a few different sets of articles. In each case, the steps for processing them was basically the same.

The first step is to use [Quarry](https://quarry.wmcloud.org/) to run a SQL query which generates a csv file with page metadata. The main datasets and corresponding queries were:
- [A sample of around 32k articles having contiguous page_random values ranging from 0.5 to 0.505](https://quarry.wmcloud.org/query/62777)
    - NB: This was before I figured out the trick of calculating random gaps directly as part of the SQL query, so this dataset required calculating the gaps as a postprocessing step, using `gaps.py`
- [Pages in the "Phaegopterina stubs" category](https://quarry.wmcloud.org/query/62881)
- [The 600k articles having the smallest random gaps](https://quarry.wmcloud.org/query/62816)

The next step is to run `get_views.py`, passing in the filename of the csv downloaded from quarry. This will create a csv having a column with article name, plus 12 columns having monthly page views in 2021 for that article, with a final convenience column having the total for the year.

`merge.py` merges the csv's from steps 1 and 2.

The subsequent analysis and visualization of the merged data is done in the included ipython notebooks.
