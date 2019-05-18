# IMPORTS
from collections import Counter
from hebrew_tokenizer import tokenize
import os
import csv
from pathlib import Path
from tqdm import tqdm
import pickle
from time import sleep


home = Path(__file__).parent


def csv2counter(save_counter_as_pickle=False):
    heb_common_words = Counter()
    tweet_count = 0
    files = os.listdir(home / 'data')
    excluded_tweets = 0
    # bad_tweets = []
    for i, f in tqdm(enumerate(files), total=len(files)):
        with open(home / 'data' / f, 'r') as c:
            try:
                tweets = csv.reader(c)
                t = next(tweets)
                for t in tweets:
                    tweet_count += 1
                    tweet = t[0]
                    if 'Youtube' in tweet or 'https:/' in tweet:
                        excluded_tweets += 1
                        continue
                    tokens = [tok[1] for tok in tokenize(tweet) if tok[0] == 'HEB' and len(tok[1]) > 1]
                    heb_common_words.update(tokens)
            except Exception as e:
                print(e)
                print(f)
    heb_common_words['total_tweets'] = tweet_count * 10
    heb_common_words['excluded_tweets'] = excluded_tweets * 10
    if save_counter_as_pickle:
        with open(home / 'results' / 'results.pkl', 'wb') as p:
            pickle.dump(heb_common_words, p)

    sleep(1)
    print(f'\ntotal tweets = {tweet_count}\nexcluded tweets = {excluded_tweets}\n')
    line_break = f'{"-"*60}\n\n'
    print(line_break)
    return heb_common_words


if __name__ == '__main__':
    tweets_counter = csv2counter()


