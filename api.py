# IMPORTS
import pandas as pd


def generate_top_n_most_common_txt_file(tweets_counter, n=1000, save_as='hebrew_most_common'):
    top_n = []

    n_most_common = tweets_counter.most_common(n+2)

    tweets_count = n_most_common[0]
    total_tweets = tweets_count[1] // 10
    total_words_in_tweets = sum(list(tweets_counter.values()))
    total_tweets_str = "{:,}".format(total_tweets)
    total_words_str = "{:,}".format(total_words_in_tweets)

    excluded_tweets_count = n_most_common[1][1] // 10
    excluded_tweets_str = "{:,}".format(excluded_tweets_count)

    header = []
    general_info = f'GENERAL INFO\n#tweets = {total_tweets_str}\n' \
                   f'#exluded tweets = {excluded_tweets_str}\n' \
                   f'#total words in tweets = {total_words_str} \n'
    print(general_info)
    header.append(general_info)
    line_break = f'{"-"*60}\n\n'
    print(line_break)
    header.append(line_break)
    mapping = 'a - word\nb - count\nc - %_of_total_words\n\n'
    header.append(mapping)

    for word, count in n_most_common[2:]:
        row = [word, count, "{:,}".format(round((count/total_words_in_tweets)*100, 2))]
        top_n.append(row)

    df = pd.DataFrame(top_n, columns=['a', 'b    ', 'c      '])

    filename = f'results/{save_as}_{n}.txt'
    with open(filename, 'w') as f:
        f.writelines(header)

    df.to_csv(filename, sep='\t', mode='a')


if __name__ == '__main__':
    import process_twitter_data
    counter = process_twitter_data.csv2counter()
    generate_top_n_most_common_txt_file(counter, n=1000)


