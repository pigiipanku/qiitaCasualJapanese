#  dfにcountとsenteceの判断を追加
import re
import pickle
import time
import json

import pandas as pd
import treetaggerwrapper as ttw

# 読み込み

# uKnow
uKnow_df = pd.read_csv(open('./format_data/uKnow.csv', 'rU'), encoding='utf-8', engine='c', index_col=0)

# countsを追加
with open('./count_list.pickle', 'rb') as f:
    counts = pickle.load(f)
uKnow_df['count'] = counts

sentence = []
# ちゃんと文になっているかどうかを確認する
tagger = ttw.TreeTagger(TAGLANG='en')
for index, row in uKnow_df.iterrows():

    try:  # 品詞を抽出
        tags = tagger.TagText(row['english'])
    except TypeError:  # Floatはスキップ
        sentence.append(False)
        continue

    # １語の時に、文章になっているかを判断する
    if len(tags) == 1:
        sentence.append(False)
    else:
        sentence.append(True)

# senteceを追加
uKnow_df['sentence'] = sentence

# countでソート
uKnow_df = uKnow_df.sort_values(by=["count"], ascending=False)

# 保存
uKnow_df.to_csv('./uKnow/uKnow2.csv')