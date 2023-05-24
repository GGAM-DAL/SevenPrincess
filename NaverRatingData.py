# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
import re

# # 네이버 영화 리뷰 데이터
# - (영화 고유 ID,댓글 ID Primary key,평점(int 0-10),공감수,비공감수,'한국어 댓글 내용')
# - https://github.com/drexly/movie140reviewcorpus

fnames = glob('./raw/*.txt')
len(fnames)

fnames

rating = []
review = []
for f in fnames[:1000]:
    file = open(f, encoding='utf-8')
    for i, line in enumerate(file.readlines()):    
        if len(line.split(',')) < 6:
            continue
        else:
            rating.append(line.split(',')[2])
            review.append(line.split(',')[-1])
        print(f+str(i)+'완료')

for f in fnames[17000:18000]:
    file = open(f, encoding='utf-8')
    for i, line in enumerate(file.readlines()):    
        if len(line.split(',')) < 6:
            continue
        else:
            rating.append(line.split(',')[2])
            review.append(line.split(',')[-1])
        print(f+str(i)+'완료')

naver = pd.DataFrame({'review':review, 'star':rating})
len(naver)

naver

naver.to_csv('naver_review.csv', encoding='utf-8')

del(rating)
del(review)
del(naver)

# ## 전처리

naver = pd.read_csv('naver_review.csv', encoding='utf-8', index_col=0, low_memory=False)

naver.info()

naver.star.unique()

# stars = ['10', '9', '1', '6', '8', '7', '5', '4', '2', '3']
naver = naver[(naver['star']=='10')|(naver['star']=='9')|(naver['star']=='8')|(naver['star']=='7')|(naver['star']=='6')|(naver['star']=='5')|(naver['star']=='4')|(naver['star']=='3')|(naver['star']=='2')|(naver['star']=='1')]
naver.star.unique()

naver

# ### csv로 내보내기

naver.to_csv('naver_review.csv', encoding='utf-8')

# ## 별점 분포 보기

naver.star.value_counts()

stars = naver.groupby('star').star.count()
plt.bar(stars.index, stars)
plt.show


# => 10점짜리 1/3로 줄이기

# ### 리뷰에 특수문자 제거하기

def clean_str(text):
    text = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", text) ## 특수기호제거
    text = re.sub('([ㄱ-ㅎㅏ-ㅣ]+)', "", text) ## 한글 자음, 모음 제거
    text = re.sub('\n', "",text)  ## \n 제거
    return text  


reviews = []
for r in naver['review']:
    reviews.append(clean_str(r))

len(reviews)

naver['review'] = reviews

naver

## 빈칸인 리뷰 행 제거
naver = naver[naver['review'] != '']
naver

naver.to_csv('naver_review_cleansing.csv', encoding='utf-8')

# ### 10점 리뷰

naver10 = naver[naver['star'] == 10]
naver10

naver10.reset_index(drop=True, inplace=True)
naver10

naver10_3 = naver10[naver10.index%3 == 0]
naver10_3

naver.drop(naver[naver['star'] == 10].index, inplace=True)
naver

naver = pd.concat([naver, naver10_3])

naver.reset_index(drop=True, inplace=True)
naver

stars = naver.groupby('star').star.count()
plt.bar(stars.index, stars)
plt.show

stars

# ### csv로 내보내기

naver.to_csv('naver_review_cleansing.csv', encoding='utf-8')
