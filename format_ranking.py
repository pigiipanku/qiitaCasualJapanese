# rakingを作成
import re
import pickle
import time

import pandas as pd

# 読み込み

# JESC
with open('./format_data/JESC_en', 'r') as f:
    JESC = f.readlines()

# uKnow
uKnow_df = pd.read_csv(open('./format_data/uKnow.csv','rU'), encoding='utf-8', engine='c', index_col=0)

# 数える
# uKnow_row
count_list = []
for uKnow_row in uKnow_df.itertuples():
    count = 0
    uKnow_words = str(uKnow_row[1]).split(' ')  # english
    uKnow_words = [uKnow_word.lower() for uKnow_word in uKnow_words]
    # JESC_row
    for JESC_row in JESC:
        i = 0
        JESC_words = JESC_row.split(' ')
        # JESC_word
        for JESC_word in JESC_words:
            # もしその単語が存在していたら、iをインクリメントしていく。違うのが間に混じっていたらもう一度０からにする
            if JESC_word == uKnow_words[i]:
                i += 1
                # 一致したらcountをインクリメント
                if len(uKnow_words) == i:
                    count += 1
                    i = 0
                    continue
            else:
                i = 0

    count_list.append(count)
    print(uKnow_row, count)

with open('count_list.pickle', 'wb') as f:
    pickle.dump(count_list, f)