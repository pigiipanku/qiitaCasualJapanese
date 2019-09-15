import pandas as pd
import pickle
from bs4 import BeautifulSoup
import requests


original_url = 'https://eikaiwa.dmm.com/uknow/daily_conversation/page:'
headers = {'User-Agent': 'Mozilla/5.0'}

all_questions = []
all_goods = []
all_views = []


for i in range(1,10000):

    url = original_url + str(i)
    print(url)

    try:
        response = requests.get(url, headers=headers)
    except:
        print(i)
        break

    soup = BeautifulSoup(response.text, 'html.parser')

    a_ = soup.find_all('div', class_='container-padding border-all-solid link')
    questions = [a.find_all('a')[0].get('href') for a in a_]

    a_ = soup.find_all('div', class_='col-lg-6 col-md-6 col-sm-12 q-list-value clearfix')
    goods = [a.find_all('p')[0].text for a in a_]
    views = [a.find_all('p')[1].text for a in a_]


    for question in questions:
        all_questions.append(question)
    for good in goods:
        all_goods.append(good)
    for view in views:
        all_views.append(view)

dic = {
    'questions' : all_questions,
    'goods' : all_goods,
    'views' : all_views
}

with open('./uKnow.pickle', 'wb') as f:
    pickle.dump(dic, f)

df = pd.DataFrame(dic)
df.to_csv('./uKnow.csv')