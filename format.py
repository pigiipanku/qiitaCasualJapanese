# rankingを作る前の前処理
import re
import pickle
import time
import json

import pandas as pd

# 読み込み

# JESC
with open('./JESC/en', 'r') as f:
    JESC = f.readlines()

# uKnow
uKnow_df = pd.read_csv(open('./uKnow/uKnow.csv','rU'), encoding='utf-8', engine='c', index_col=0)

with open('./omission.json', 'r') as f:
    omission_dict = json.load(f)

# データ整形
# JESC
new_JESC = []
print("JESC:", len(JESC))
for JESC_row in JESC:

    # 小文字にする
    JESC_row = str(JESC_row).lower()

    # 省略形を正規化
    for key, value in omission_dict.items():
        JESC_row = JESC_row.replace(key, value)

    JESC_words = JESC_row.split(' ')
    JESC_replace_words = []

    for JESC_word in JESC_words:
        # 0~9.,?!などを消す
        JESC_word = re.sub(r"[^a-zA-Z']", "", JESC_word)

        # 空文字じゃなかったら入レル
        if JESC_word:
            JESC_replace_words.append(JESC_word)

    # 置き換える
    new_JESC.append(" ".join(JESC_replace_words))

print("new_JESC", len(new_JESC))
with open('./format_data/JESC_en', 'w') as f:
    for JESC_row in new_JESC:
        f.write(JESC_row + "\n")

# uKnow
new_uKnow = []
print("uKnow:", len(uKnow_df))
for index, uKnow_row in uKnow_df.iterrows():

    # 小文字にする
    uKnow_row = str(uKnow_row[0]).lower()

    # 省略形を正規化
    for key, value in omission_dict.items():
        uKnow_row = uKnow_row.replace(key, value)

    uKnow_words = uKnow_row.split(' ')
    uKnow_replace_words = []

    for uKnow_word in uKnow_words:
        # 0~9.,?!などを消す
        uKnow_word = re.sub(r"[^a-zA-Z']", "", uKnow_word)

        # 空文字じゃなかったら入れる
        if uKnow_word:
            uKnow_replace_words.append(uKnow_word)

    # 置き換える
    uKnow_df.at[index, 'english'] = " ".join(uKnow_replace_words)

print(len(uKnow_df.drop_duplicates(subset='english')))
uKnow_df.to_csv('./format_data/uKnow.csv')