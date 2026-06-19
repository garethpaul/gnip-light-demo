# Let's take off from where we were before and output the bliebers to a CSV
from gnip_search.tweets import FullArchiveSearch
import csv
import os
import sys
import tempfile


def main(output_path='bliebers.csv'):
    query_count = 10000  # int(request.GET.get("embedCount", TWEET_QUERY_COUNT))
    query = "#JustinBieber"
    tweets = FullArchiveSearch(query=query, query_count=query_count)
    results = tweets.get_data()
    output_directory = os.path.dirname(os.path.abspath(output_path))
    descriptor, temporary_path = tempfile.mkstemp(
        prefix=".bliebers-", suffix=".csv", dir=output_directory)
    csvfile = None
    try:
        if sys.version_info[0] < 3:
            csvfile = os.fdopen(descriptor, 'wb')
        else:
            csvfile = os.fdopen(descriptor, 'w', newline='')
        bieber_writer = csv.writer(csvfile,
                                   delimiter=',',
                                   quotechar='|',
                                   quoting=csv.QUOTE_MINIMAL)
        for tweet in results:
            user_id = tweet['actor']['id']
            bieber_writer.writerow([user_id.strip("id:twitter.com:")])
        csvfile.flush()
        os.fsync(csvfile.fileno())
        csvfile.close()
        csvfile = None
        os.rename(temporary_path, output_path)
    finally:
        if csvfile is not None:
            csvfile.close()
        if os.path.exists(temporary_path):
            os.unlink(temporary_path)


if __name__ == "__main__":
    main()
