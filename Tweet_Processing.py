"""
A script for processing Tweets
"""

import numpy as np
import pandas as pd
import sklearn.feature_extraction.text as text
import re

df1 = pd.read_csv("./data/sarw.csv")
df2 = pd.read_csv("./data/info.csv")
df3 = pd.read_csv("./data/uscg.csv")
df4 = pd.read_csv("./data/last_week.csv")

df = pd.concat([df1, df2, df3, df4])

tweetlist = df['Tweet'].tolist()

# delete links
for i in range(len(tweetlist)):
    tweetlist[i] = re.sub(r'https\S+', '', tweetlist[i])

    if tweetlist[i].startswith('RT'):
        tweetlist[i] = tweetlist[i][3:]

def ng(t_input, max_features, ngram):
    """
    Returns the top ngram words in a list of tweets.
    The aim is to see what words and word combinations appear to be the most common in the reports.
    

    Parameters
    ----------
    tweetlist : list
        A list of tweets
    max_features : int
        The maximum number of features to be used
    ngram : int
        The number of words to be used in the ngram

    Returns
    -------
    pd.Series
        A pandas series of the top ngram words in the list of tweets
    
    """
    tfidf = text.CountVectorizer(
        input = t_input, 
        ngram_range = (ngram, ngram),
        max_features = max_features,
        stop_words = 'english'
        )
    matrix = tfidf.fit_transform(t_input)
    
    return pd.Series(
        np.array(matrix.sum(axis = 0))[0],
        index = tfidf.get_feature_names_out()
        ).sort_values(ascending = False).head(100)

dm = []
dates = []

for tweet, date in zip(df['Tweet'], df['Date']):
    if 'migrant' in tweet or 'migrants' in tweet:
        if 'dead' in tweet or 'died' in tweet or 'death' in tweet or 'bodies' in tweet or 'missing' in tweet:
            dm.append(tweet)
            dates.append(date)

unigrams = ng(
    t_input = dm,
    max_features = 5000,
    ngram = 1
    )
bigrams = ng(
    t_input = dm,
    max_features = 5000,
    ngram = 2
    )
trigrams = ng(
    t_input = dm,
    max_features = 5000,
    ngram = 3
    )

# printing the most common words and word combinations in the tweets to get an idea of what kind of wording is used in reports
print(unigrams.head(20))
print(bigrams.head(20))
print(trigrams.head(20))

# print Tweets and dates for manual inspection
for t,d in zip(dm, dates):
    print('Tweet: ' + t + ' Date: ' + d)

# manually inputting data gathered by reading processed Tweets 
data_list = [ 
    {'route' : 'Central Mediterranean', 'location' : 'Mahdia coast, Tunisia', 'number dead' : '15', 'number missing' : '0', 'date' : '2022-10-14', 'lat' : '35.513919', 'lon' : '11.090457'},
    {'route' : 'Central Mediterranean', 'location' : 'Trapani, Sicily', 'number dead' : '3', 'number missing' : '0', 'date' : '2022-10-13', 'lat' : '38.034506', 'lon' : '12.476485'},
    {'route' : 'Central Mediterranean', 'location' : 'Zarzis, Tunisia', 'number dead' : '11', 'number missing' : '0', 'date' : '2022-09-21', 'lat' : '33.509019', 'lon' : '11.134580'},
    {'route' : 'Central Mediterranean', 'location' : 'Sbaratha, Libya', 'number dead' : '15', 'number missing' : '0', 'date' : '2022-10-07', 'lat' : '32.874355', 'lon' : '12.461700' },
    {'route' : 'Eastern Mediterranean', 'location' : 'Kythira, Greece', 'number dead' : '23', 'number missing' : '0', 'date' : '2022-10-05', 'lat' : '36.245586', 'lon' : '23.161616'},
    {'route' : 'Eastern Mediterranean', 'location' : 'Lesbos', 'number dead' : '16', 'number missing' : '0', 'date' : '2022-10-06', 'lat' : '39.239494', 'lon' : '26.517556'},
    {'route' : 'Western Mediterranean', 'location' : 'Spain / Canary Islands', 'number dead' : '4', 'number missing' : '0', 'date' : '2022-10-06', 'lat' : '28.652163', 'lon' : '-15.661686'},
    {'route' : 'Eastern Mediterranean', 'location' : 'Syria, near Arida Border', 'number dead' : '97', 'number missing' : '0', 'date' : '2022-09-26', 'lat' : '34.633319', 'lon' : '35.973976'},
    {'route' : 'Eastern Mediterranean', 'location' : 'Aegean Sea, Turkey', 'number dead' : '6', 'number missing' : '0', 'date' : '2022-09-15', 'lat' : '38.083909', 'lon' : '25.454807'},
    {'route' : 'Eastern Mediterranean', 'location' : 'Turkey, coast of Izmir', 'number dead' : '6', 'number missing' : '5', 'date' : '2022-09-15', 'lat' : '38.437494', 'lon' : '27.070782'},
    {'route' : 'Western Mediterranean', 'location' : 'Morocco, Tarfaya', 'number dead' : '1', 'number missing' : '0', 'date' : '2022-09-13', 'lat' : '27.959682', 'lon' : '-12.933955'},
    {'route' : 'Central Mediterranean', 'location' : 'Pozzallo, Sicily', 'number dead' : '6', 'number missing' : '0', 'date' : '2022-09-10', 'lat' : '36.723665', 'lon' : '14.854199'},
    {'route' : 'Central Mediterranean', 'location' : 'Tunisia, Chebba', 'number dead' : '8', 'number missing' : '15', 'date' : '2022-09-09', 'lat' : '35.238334', 'lon' : '11.184468'},
    {'route' : 'Eastern Mediterranean', 'location' : 'Crete, Greece', 'number dead' : '1', 'number missing' : '0', 'date' : '2022-09-08', 'lat' : '34.705937', 'lon' : '24.399454'},
    {'route' : 'Eastern Mediterranean', 'location' : 'Lebanon, Tripoli', 'number dead' : '30', 'number missing' : '0', 'date' : '2022-04-24', 'lat' : '34.469548', 'lon' : '35.790515'},
    {'route' : 'Iran to Türkiye', 'location' : 'Turkey, Van', 'number dead' : '1', 'number missing' : '0', 'date' : '2022-08-26', 'lat' : '38.502345', 'lon' : '43.235299'},
    {'route' : 'Western Mediterranean', 'location' : 'Canary Islands, Fuerteventura', 'number dead' : '3', 'number missing' : '0', 'date' : '2022-08-16', 'lat' : '28.124122', 'lon' : '-13.638271'},
    {'route' : 'Sahara Desert crossing', 'location' : 'Libya, North Darfur, Libya-Sudan border,', 'number dead' : '15', 'number missing' : '2', 'date' : '2022-08-15', 'lat' : '20.193175', 'lon' : '24.422461'},
    {'route' : 'Western Mediterranean', 'location' : 'Algerian coast, Baïnem', 'number dead' : '6', 'number missing' : '0', 'date' : '2022-08-09', 'lat' : '36.824771', 'lon' : '2.969724'},
    {'route' : 'Western Mediterranean', 'location' : 'Morocco, Akhfennir', 'number dead' : '8', 'number missing' : '0', 'date' : '2022-07-26', 'lat' : '28.099619', 'lon' : '-12.053869'},
    {'route' : 'Sahara Desert crossing', 'location' : 'Niger, near Dirkou', 'number dead' : '10', 'number missing' : '0', 'date' : '2022-07-01', 'lat' : '20.023729', 'lon' : '13.161012'},
    {'route' : 'Central Mediterranean', 'location' : 'Italy, 200km off the Calabrian coast', 'number dead' : '5', 'number missing' : '0', 'date' : '2022-07-25', 'lat' : '36.856427', 'lon' : '17.276735'},
    {'route' : 'Sahara Desert crossing', 'location' : 'Libya, Kufra, Libya-Chad border', 'number dead' : '20', 'number missing' : '0', 'date' : '2022-06-30', 'lat' : '21.253623', 'lon' : '21.408366'},
    {'route' : 'Central Mediterranean', 'location' : 'Central Mediterranean', 'number dead' : '1', 'number missing' : '22', 'date' : '2022-06-27', 'lat' : '34.844949', 'lon' : '17.664421'},
    {'route' : 'US-Mexico border crossing', 'location' : 'US, San Antonio', 'number dead' : '46', 'number missing' : '0', 'date' : '2022-06-28', 'lat' : '29.385168', 'lon' : '-98.508756'},
    {'route' : 'Central Mediterranean', 'location' : 'Morocco, Melilla Border)', 'number dead' : '23', 'number missing' : '0', 'date' : '2022-06-28', 'lat' : '35.288345', 'lon' : '-2.959516'},
    {'route' : 'Eastern Mediterranean', 'location' : 'Greece, From Türkiye to Lesbos,', 'number dead' : '2', 'number missing' : '0', 'date' : '2022-06-27', 'lat' : '39.247488', 'lon' : '26.588229'},
    {'route' : 'Central Mediterranean', 'location' : 'Tunisia, Skhira', 'number dead' : '12', 'number missing' : '0', 'date' : '2022-06-20', 'lat' : '34.285009', 'lon' : '10.107038'},
    {'route' : 'Central Mediterranean', 'location' : 'Tunisia, Coast of Sfax', 'number dead' : '4', 'number missing' : '0', 'date' : '2022-06-21', 'lat' : '34.687726', 'lon' : '10.814120'},
    {'route' : 'Eastern Mediterranean', 'location' : 'Greece, Aegean sea, 2 miles southeast of Delos', 'number dead' : '0', 'number missing' : '8', 'date' : '2022-06-20', 'lat' : '37.370551', 'lon' : '25.296742'},
    {'route' : 'Western Mediterranean', 'location' : 'Spain, near Escombreras', 'number dead' : '4', 'number missing' : '0', 'date' : '2022-06-09', 'lat' : '37.537481', 'lon' : '-0.910363'},
    {'route' : 'Caribbean to US', 'location' : 'Islamorada', 'number dead' : '0', 'number missing' : '1', 'date' : '2022-09-02', 'lat' : '24.903589', 'lon' : '-80.608638'}]


tweet_df = pd.DataFrame.from_dict(data_list)

tweet_df['date'] = pd.to_datetime(tweet_df['date'])
tweet_df['number dead'] = tweet_df['number dead'].astype(int)
tweet_df['number missing'] = tweet_df['number missing'].astype(int)

# data after August
tweet_df = tweet_df.loc[(tweet_df['date'] >= '2022-08-01')]

# save dataframe to csv
tweet_df.to_csv('data.csv', index = False)
