from textblob import TextBlob
from newspaper import Article

# url = 'https://finance.yahoo.com/news/bitcoin-dumps-elon-musk-fails-201139388.html'
# article = Article(url)

# article.download()
# article.parse()
# article.nlp()

# text = article.text
# print(text)

# blob = TextBlob(text)
# sentiment = blob.sentiment.polarity
# print(sentiment)


##### Read Text #######
with open('sentiment.txt', 'r') as f:
    text = f.read()

blob = TextBlob(text)
sentiment = blob.sentiment.polarity
print(sentiment)





