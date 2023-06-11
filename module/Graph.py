import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import platform
import module.database as Database
import matplotlib.ticker as ticker

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

def Score(code, avg_score):
    score_df = Database.db('movie_review')
    score_df = score_df[score_df.code == code]

    ## multi selecet
    options = st.multiselect('',
                            ['blog', 'daum', 'lotte'],
                            ['blog','daum','lotte'])
    
    score_df.drop(score_df[score_df['date']>'2023-05-30'].index, axis=0, inplace=True)
    if code==1:
        score_df.drop(score_df[score_df['date']>'2017-12-19'].index, axis=0, inplace=True)
    elif code==7:
        score_df.drop(score_df[score_df['date']>'2022-10-07'].index, axis=0, inplace=True)
    elif code==8:
        score_df.drop(score_df[score_df['date']>'2022-11-04'].index, axis=0, inplace=True)
    elif code==9:
        score_df.drop(score_df[score_df['date']>'2019-09-07'].index, axis=0, inplace=True)
    elif code==10:
        score_df.drop(score_df[score_df['date']>'2016-08-20'].index, axis=0, inplace=True)
    score_df.drop(score_df[(score_df['after_release']<0)&(score_df['source']=='daum')].index, axis=0, inplace=True)
    score_df.drop(score_df[(score_df['after_release']<0)&(score_df['source']=='lotte')].index, axis=0, inplace=True)
    score_df.sort_values(by='after_release', inplace=True)
    score_df.reset_index(drop=True, inplace=True)
    
    ## 누적 평점 계산
    sites = ['blog', 'daum', 'lotte']
    score = pd.DataFrame()
    days = score_df['after_release'].max()
    if days == -7:
        days = 0
    for site in sites:
        score_one = score_df[score_df['source']==site]
        score_l = []
        days_l = []
        for d in range(-7, days+1):
            df = score_one[score_one['after_release']<=d]
            scores = df.star.mean()
            if np.isnan(scores):
                scores = 0
            score_l.append(scores)
            days_l.append(d)
        score[site]=score_l
    score['days']=days_l
    

    st.markdown("<h5><center>상영 기간 동안의 평점 변화</center></h4>", unsafe_allow_html=True)
    colors = {'blog':'green','daum':'blue','lotte':'red'}

    fig, _ = plt.subplots(figsize=(10,5))
    for i in range(len(options)):
        plt.plot(score.days, score[options[i]], 
                 linewidth=2, 
                 label=options[i], color=colors[options[i]])
    week = len(days_l)//7
    week_l1 = [-7,0,1,3]
    week_l2 = ['개\n봉\n전','개\n봉','1\n일\n차','3\n일\n차']
    for i in range(1,week+1):
        week_l1.append(i*7)
        week_l2.append(str(i)+'\n주\n차')
    plt.xticks(week_l1,week_l2)
    plt.ylim(0,10)
    plt.axvline(x = 0, color='black', linewidth=1)
    plt.axhline(y = avg_score, color='pink', linestyle='--', linewidth=1)

    plt.legend()
    st.pyplot(fig)
    st.markdown("<h5><center>선택 사이트의 종합 평점 분포도</center></h4>", unsafe_allow_html=True)

    fig, _ = plt.subplots(figsize=(10,5))
    hist_df = pd.DataFrame([], columns=['title','review', 'star', 'date', 'release', 'code', 'screening', 'source', 'after_release'])
    for o in options:
        hist_df1 = score_df[score_df['source'] == o]
        hist_df = pd.concat([hist_df, hist_df1])
    hist_df = hist_df.groupby('star').count()
    plt.bar(hist_df.index, hist_df.title, color = 'pink')
    # y 축에 천 단위로 콤마 표시
    formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x))
    plt.gca().yaxis.set_major_formatter(formatter)
    st.pyplot(fig)



def Audience(code, screening):


    if screening == 0:
        html="<h1 style='text-align:center;'>Before Release</h1>"
        st.markdown(html, unsafe_allow_html=True)
        return
    
    audi_df = Database.db('accum_audi')
    audi = audi_df[audi_df.code == code].reset_index(drop=True)
    audi['acc_audi'] = audi['acc_audi'].astype('int')
    audi['daily_audi'] = audi['daily_audi'].astype('int')
    
    max1 = audi['daily_audi'].max()
    max2 = audi['acc_audi'].max()

    if screening == 1:
        audi = audi[audi['date'] < '2023-05-31']
    audi = audi[audi.after_release>=0].reset_index(drop=True)

    # 슬라이드
    x = st.slider('슬라이드를 움직여 원하는 날까지 관객수를 보세요', value=21,
                  min_value=0, max_value=audi.shape[0]-1, step=1)
    df = audi[audi.after_release<=x]

    # 그래프
    fig, ax1 = plt.subplots(figsize=(12,5))
    ax2 = ax1.twinx()
    ax1.bar( df.after_release, df.daily_audi)
    ax2.plot(df.after_release, df.acc_audi, color='#FF4B4B', linewidth=3)

    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])

    # x축
    week = df.shape[0]//7
    week_l1 = [0,1,3]
    week_l2 = ['개\n봉','1\n일\n차','3\n일\n차']
    for i in range(1,week+1):
        week_l1.append(i*7)
        week_l2.append(str(i)+'\n주\n차')
    plt.xticks(week_l1,week_l2)
    # y 축에 천 단위로 콤마 표시
    formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x))
    plt.gca().yaxis.set_major_formatter(formatter)
    st.pyplot(fig)

    col1, col2 = st.columns(2)

    
    with col1:
        html=f"""
<style>
    .box {{
        width:100%;
        border: 1px solid black;
        border-collapse: separate !important;
        -moz-border-radius: 10px;
        -webkit-border-radius: 10px;
        border-radius: 10px;
        margin:5px;
        }}
    .review {{margin:3px; margin-left:10px;}}
    .num {{
        font-weight:bold;
        font-size:20px;
    }}
</style>
<body>
    <div class='box'>
        <div class='review'>
            <h5><center>일일 최대 관객수</center></h5>
            <center class="num">{max1} 명</center>
        </div>
    </div>
</body>
        """
        st.markdown(html, unsafe_allow_html=True)
    with col2:
        html=f"""
<style>
    .box {{
        width:100%;
        border: 1px solid black;
        border-collapse: separate !important;
        -moz-border-radius: 10px;
        -webkit-border-radius: 10px;
        border-radius: 10px;
        margin:5px;
        }}
    .review {{margin:3px; margin-left:10px;}}
    .num {{
        font-weight:bold;
        font-size:20px;
    }}
</style>
<body>
    <div class='box'>
        <div class='review'>
            <h5><center>누적 관객수</center></h5>
            <center class="num">{max2} 명</center>
        </div>
    </div>
</body>
        """
        st.markdown(html, unsafe_allow_html=True)