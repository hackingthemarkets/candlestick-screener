from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import requests
import bs4

news_tables = []

url = requests.get('https://finance.yahoo.com/topic/crypto/').text

#title = bs4.BeautifulSoup(url, "html.parser")
#html = bs(url.content, features='html.parser')
html = bs(url, 'lxml')

#row = html.find('ul', class_='My(0) Ov(h) P(0) Wow(bw)')
#li = row.find_all('li', class_='js-stream-content Pos(r)')
parsed_data = []
try: 
    for each_row in html.find_all('li', class_='js-stream-content Pos(r)'):
        
        h3 = each_row.a.text
        parsed_data.append(h3)
        #print(h3)

        #content = each_row.p.text

        # paragragh = each_row.find('p', class_='Fz(14px) Lh(19px) Fz(13px)--sm1024 Lh(17px)--sm1024 LineClamp(2,38px) LineClamp(2,34px)--sm1024 M(0)')
        # content = paragragh.text
        #print(content)

        
except Exception as e:
    print('Error: ', str(e))

df = pd.DataFrame(parsed_data, columns=['title'])

vader = SentimentIntensityAnalyzer()
f = lambda title: vader.polarity_scores(title)['compound']
compound = df['title'].apply(f)

df2 = df.assign(sentimental = compound)

print(df2)

# plt.figure(figsize=(10,8))
# mean_df = df.groupby(['title']).mean().unstack()
# mean_df = mean_df.xs('compound', axis="columns")
# mean_df.plot(kind='bar')
# plt.show()





# for ticker in tickers:
#     url = finviz_url + ticker

#     req = Request(url=url, headers={'user-agent': 'my-app'})
#     response = urlopen(req)

#     html = BeautifulSoup(response, features='html.parser')
#     news_table = html.find(id='news-table')
#     news_tables[ticker] = news_table

# parsed_data = []

# for ticker, news_table in news_tables.items():

#     for row in news_table.findAll('tr'):

#         title = row.a.text
#         date_data = row.td.text.split(' ')

#         if len(date_data) == 1:
#             time = date_data[0]
#         else:
#             date = date_data[0]
#             time = date_data[1]

#         parsed_data.append([ticker, date, time, title])

# df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

# vader = SentimentIntensityAnalyzer()

# f = lambda title: vader.polarity_scores(title)['compound']
# df['compound'] = df['title'].apply(f)
# df['date'] = pd.to_datetime(df.date).dt.date

# plt.figure(figsize=(10,8))
# mean_df = df.groupby(['ticker', 'date']).mean().unstack()
# mean_df = mean_df.xs('compound', axis="columns")
# mean_df.plot(kind='bar')
# plt.show()