from google.colab import drive
drive.mount('/content/drive')

import zipfile
import os

zip_path = '/content/drive/My Drive/archive.zip'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('/content/dataset')

import pandas as pd

csv_file_path = '/content/dataset/twcs/twcs.csv'

df = pd.read_csv(csv_file_path)

print(df.head())

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Analysis and Visualization

# Frequency of tweets over time
df['created_at'] = pd.to_datetime(df['created_at'])
df.set_index('created_at', inplace=True)
df.resample('D').size().plot()
plt.title('Tweet Frequency Over Time')
plt.ylabel('Number of tweets')
plt.show()


# Top authors by tweet count

top_authors = df['author_id'].value_counts().head(10)
sns.barplot(x=top_authors.index, y=top_authors.values)
plt.title('Top 10 Authors by Tweet Count')
plt.ylabel('Number of Tweets')
plt.xlabel('Author ID')
plt.xticks(rotation=45)
plt.show()




# Sentiment Analysis

from textblob import TextBlob

def calculate_sentiment(text):
    return TextBlob(text).sentiment.polarity

df['sentiment'] = df['text'].apply(calculate_sentiment)

sns.histplot(df['sentiment'], bins=30)
plt.title('Sentiment Distribution')
plt.show()

# LDA analysis

import pandas as pd
from gensim import corpora, models
import gensim
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

df['clean_text'] = df['text'].str.lower().str.replace('[^\w\s]', '')
stop_words = set(stopwords.words('english'))
df['clean_text'] = df['clean_text'].apply(lambda x: ' '.join(word for word in x.split() if word not in stop_words))


text_data = [text.split() for text in df['clean_text']]
dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]

lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)
lda_model.print_topics()

import pyLDAvis.gensim_models as gensimvis
import pyLDAvis

pyLDAvis.enable_notebook()
lda_vis = gensimvis.prepare(lda_model, corpus, dictionary)
pyLDAvis.display(lda_vis)


# Generating a word cloud

from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(background_color='white').generate(' '.join(df['clean_text']))
plt.figure(figsize=(10, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()


# Analysis of hashtags

import re

def extract_hashtags(s):
    return re.findall(r'#(\w+)', s)

def extract_mentions(s):
    return re.findall(r'@(\w+)', s)

df['hashtags'] = df['text'].apply(extract_hashtags)
df['mentions'] = df['text'].apply(extract_mentions)

all_hashtags = sum(df['hashtags'], [])
pd.Series(all_hashtags).value_counts().head(10).plot(kind='bar')
plt.title('Top 10 Hashtags')
plt.show()



df['created_at'] = pd.to_datetime(df['created_at'])


# Plotting the trend

tweets_per_day = df.resample('D', on='created_at').count()


plt.figure(figsize=(12, 6))
plt.plot(tweets_per_day.index, tweets_per_day['text'], label='Number of Tweets')
plt.title('Trend of Tweets Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Tweets')
plt.legend()
plt.show()
