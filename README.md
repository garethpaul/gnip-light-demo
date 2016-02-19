# GNIP Demo

Getting started

```pip install -r requirements.txt```

Simple usage of FullArchive search e.g.

```
from gnip_search.tweets import FullArchiveSearch

query_count = 10000  # int(request.GET.get("embedCount", TWEET_QUERY_COUNT))
export = None
query = "#JustinBieber"
tweets = FullArchiveSearch(query=query, query_count=query_count)
print tweets.get_data()
```
