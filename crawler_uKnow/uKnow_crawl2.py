import pickle
import re

import pandas as pd
from bs4 import BeautifulSoup
import requests

def turn_off_japanese(japanese):

    japanese = re.sub(r'[!-~]', "", japanese)#半角記号,数字,英字
    japanese = re.sub(r'[︰-＠]', "", japanese)#全角記号
    japanese = re.sub('\n', " ", japanese)#改行文字

    return japanese


if __name__ == "__main__":

    original_url = "https://eikaiwa.dmm.com"
    headers = {'User-Agent': 'Mozilla/5.0'}
    all_japanese = []
    all_english = []
    all_goods = []
    all_views = []
    all_url = []

    df = pd.read_csv('./uKnow.csv')

    for index, row in df.iterrows():
        print(row[1])

        url = original_url + row[1]
        print(index, url)

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 英語
        try:
            english = soup.find('span', class_='answer').text
        except:
            continue


        # 日本語
        try:
            japanese = soup.find_all('h1', id="question-title")[0].text.split("って英語で")[0]
        except:
            continue
        japanese = turn_off_japanese(japanese)

        all_english.append(english)
        all_japanese.append(japanese)
        all_goods.append(row[2])
        all_views.append(row[3])
        all_url.append(url)

    df = pd.DataFrame({'english': all_english,
                       'japanese': all_japanese,
                       'good': all_goods,
                       'view': all_views,
                       'url': all_url})

    df.to_csv('./uKnow2.csv')