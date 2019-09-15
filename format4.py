# sentence=Trueを排除
# 重複も削除
import re
import pickle
import time
import json

import pandas as pd
import treetaggerwrapper as ttw

# 読み込み

# uKnow
uKnow_df = pd.read_csv(open('./uKnow/uKnow2.csv', 'rU'), encoding='utf-8', engine='c', index_col=0)

# １語を削除
uKnow_df = uKnow_df[uKnow_df['sentence'] != True]

# 重複を削除
uKnow_df = uKnow_df[~uKnow_df.duplicated(subset=['english'], keep='first')]

# 保存
uKnow_df.to_csv('./uKnow/uKnow4.csv')
