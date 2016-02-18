# Let's take off from where we were before and output the bliebers to a CSV
from gnip_search.tweets import FullArchiveSearch
import csv

query_count = 10000  # int(request.GET.get("embedCount", TWEET_QUERY_COUNT))
export = None
query = "#JustinBieber"
tweets = FullArchiveSearch(query=query, query_count=query_count)
with open('bliebers.csv', 'wb') as csvfile:
    bieber_writer = csv.writer(csvfile,
                               delimiter=',',
                               quotechar='|',
                               quoting=csv.QUOTE_MINIMAL)
    for tweet in tweets.get_data():
        user_id = tweet['actor']['id']
        bieber_writer.writerow([user_id.strip("id:twitter.com:")])
