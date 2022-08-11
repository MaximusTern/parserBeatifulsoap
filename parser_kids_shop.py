import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = 'https://www.gulliver.ru/catalog/odezhda/b/gulliver?sort=our_choice,asc'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

head_url = soup.find_all('button', class_="card__like like-btn js-like-btn" )
head_card = soup.find_all('div', class_="catalog-block__card")

data = {}
for item in head_card:
    article_id = item.find('button', class_="card__like like-btn js-like-btn").get('data-product_article')
    url = item.find('a').get('href')
    name = item.find('span', class_="card__title-text").text
    name = re.sub("^\s+|\n|\r|\s+$", '', name)
    old_price = item.find('span', class_="price__inner--old").get_text()
    new_price = item.find('span', class_="price__inner--new").get_text()
    data[article_id]=name, old_price, new_price, url
print(data)
columns = ['name', 'oldprice', 'newprice','url']
df_pars = pd.DataFrame.from_dict(data,orient='index', columns=columns)
df_pars['article'] = df_pars.index
df_pars.reset_index(drop=True, inplace=True)
print(df_pars)

