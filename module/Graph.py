import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import platform
import module.database as Database

# 한글 폰트 지정
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False

if platform.system() == 'Darwin':  # 맥OS
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # 윈도우
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system...  sorry~~~')

def Score(code):
    score_df = Database.db('suzume')
    score_df = score_df[score_df.code == code]
    
    st.subheader('Movie Rate!')
    ## multi selecet
    options = st.multiselect('Choose the site you want to SEE! ',
                            ['Blog', 'Watcha', 'Daum', 'Lotte'],
                            ['Blog', 'Watcha'])

    st.write('You selected:', options)

    ## 누적 평점 계산
    score = pd.DataFrame(columns=['star','days'])
    score_l = []
    days_l = []
    days = score_df.after_release.unique()
    for d in days:
        df = score_df[score_df['after_release']<=d]
        score_l.append(df['star'].sum(axis=0) / df.shape[0])
        days_l.append(d)
    score['star']=score_l
    score['days']=days_l

    fig, _ = plt.subplots(figsize=(12,5))
    plt.plot(score.days, score.star, color='#FF4B4B')
    # for i in range(0,x,10):
    #     plt.text(i, i, df.iloc[i]['acc_audi'],horizontalalignment='center' )
    # plt.gca().axes.yaxis.set_visible(False)
    # plt.xticks([21], ['3주차'])
    # plt.xticks([0,1,3,7,14,21,28,35,42],['개봉','1일차','3일차','1주차','2주차','3주차','4주차','5주차','6주차'])
    st.pyplot(fig)


def Audience(code, screening):
    st.subheader('Audience')
    if screening == 0:
        html="<h1 style='text-align:center;'>Before Release</h1>"
        st.markdown(html, unsafe_allow_html=True)
        return

    audi_df = Database.db('accum_audi')
    audi = audi_df[audi_df.code == code].reset_index(drop=True)
    if screening == 1:
        audi = audi[audi['date'] < '2023-05-31']
    audi = audi[audi.after_release>=0]

    
    x = st.slider('Day of Release', value=21,
                  min_value=0, max_value=audi.shape[0]-1, step=1)
    df = audi[audi.after_release<=x]
    fig, _ = plt.subplots(figsize=(12,5))
    plt.plot(df.after_release, df.acc_audi, color='#FF4B4B')
    for i in range(0,x,10):
        plt.text(i, i, df.iloc[i]['acc_audi'],horizontalalignment='center' )
    plt.gca().axes.yaxis.set_visible(False)
    # plt.xticks([21], ['3주차'])
    # plt.xticks([0,1,3,7,14,21,28,35,42],['개봉','1일차','3일차','1주차','2주차','3주차','4주차','5주차','6주차'])
    st.pyplot(fig)