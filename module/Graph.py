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
    options = st.multiselect('평점의 변화를 확인하고 싶은 사이트를 선택하세요',
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
    

    st.markdown("<h5><center>상영 기간 동안의 평점 변화</center></h5>", unsafe_allow_html=True)
    colors = {'blog':'green','daum':'blue','lotte':'red'}

    fig, _ = plt.subplots(figsize=(10,5))
    for i in range(len(options)):
        plt.plot(score.days, score[options[i]], 
                 linewidth=2, 
                 label=options[i], color=colors[options[i]], zorder=1)
        
    week = len(days_l)//7
    week_l1 = [-7,0,1,3]
    week_l2 = ['개\n봉\n전','개\n봉','1\n일\n차','3\n일\n차']

    for i in range(1,week):
        week_l1.append(i*7)
        week_l2.append(str(i)+'\n주\n차')
    plt.xticks(week_l1,week_l2)
    plt.ylim(0,10)

    ## 실선
    plt.axvline(x = 0, color='black', linestyle='--',linewidth=1, zorder=0)
    plt.axhline(y = avg_score, color='pink', linestyle='--', linewidth=1, zorder=2)

    plt.legend()
    st.pyplot(fig)

    site_dict = {'blog':'네이버 블로그', 'daum':'다음 영화','lotte':'롯데시네마'}
    if len(options) == 1:
        site = site_dict[options[0]]
    elif len(options) == 2:
        site = f"{site_dict[options[0]]}, {site_dict[options[1]]}"
    else:
        site = '전체 사이트'

    html = f"""
    <br><br>
    <h5><center>{site}의 평점 분포도</center></h5>
    """
    st.markdown(html, unsafe_allow_html=True)

    fig, _ = plt.subplots(figsize=(10,5))
    hist_df = pd.DataFrame([], columns=['title','review', 'star', 'date', 'release', 
                                        'code', 'screening', 'source', 'after_release'])
    for o in options:
        hist_df1 = score_df[score_df['source'] == o]
        hist_df = pd.concat([hist_df, hist_df1])
    hist_df = hist_df.groupby('star').count()
    colors = []
    for i in hist_df.index:
        if i < 7:
            colors.append('b')
        else:
            colors.append('r')
    plt.bar(hist_df.index, hist_df.title, color = colors, alpha=0.7)
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10])
    # y 축에 천 단위로 콤마 표시
    formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x))
    plt.gca().yaxis.set_major_formatter(formatter)
    st.pyplot(fig)
    
    html = """
    <style>
        .bar_info {
            text-align: right;
            font-size: 7px;
            color: gray;
        }
    </style>
    <div text-aligh='left'>
    <p class='bar_info'>⭐붉은 막대 그래프는 <span style='color: red; alpha: 0.7;'>긍정 </span>, 
    푸른 막대 그래프는 <span style='color: blue; alpha: 0.7;'>부정 </span>평점</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)



def Audience(code, screening):

    if screening == 0:
        df = Database.db('lv_pred')
        df = df[df['code']==code]
        pred = df.iloc[0]['pred']
        if pred == '대흥행':
            s = '🥳 대흥행 예상'
        elif pred == '흥행':
            s = '😎 흥행 예상'
        elif pred == '미흥행':
            s = '😥 미흥행 예상'
        html=f"""
        <style>
            .prediction {{
                text-align:center;
                font-size: 100px;
                font-weight: bold;
            }}
        </style>
        <br><br>
        <p class='prediction'>{s}</p>"""
        st.markdown(html, unsafe_allow_html=True)
        return
    
    audi_df = Database.db('accum_audi')
    pred_df = Database.db('audi_pred')
    audi = audi_df[audi_df.code == code].reset_index(drop=True)
    pred = pred_df[pred_df.code == code].reset_index(drop=True)

    audi['acc_audi'] = audi['acc_audi'].astype('int')
    audi['daily_audi'] = audi['daily_audi'].astype('int')
    pred['pred'] = pred['pred'].astype('int')

    # max1 = audi['daily_audi'].max()
    # max2 = audi['acc_audi'].max()

    if screening == 1:
        audi = audi[audi['date'] < '2023-05-31']
    audi = audi[audi.after_release>=0].reset_index(drop=True)

    audi_x = pred.iloc[0]['pred']

    if audi.iloc[-1]['acc_audi'] >= audi_x:
        audi_y = audi[audi['acc_audi'] >= audi_x]
    else:
        audi_y = audi.iloc[[-1]]
    st.write(audi_y)
    # 슬라이드
    x = st.slider('슬라이드를 움직여 개봉일로부터 선택한 일까지의 관객수를 확인하세요', value=21,
                  min_value=0, max_value=audi.shape[0]-1, step=1)
    df = audi[audi.after_release<=x]

    # 그래프
    fig, ax1 = plt.subplots(figsize=(12,5))
    # 반대 y축 생성
    ax2 = ax1.twinx()
    # 일일 관객수 바차트
    barplot = ax1.bar( df.after_release, df.daily_audi, label = '일일 관객수')

    if x >= audi_y.iloc[0]['after_release']:
        # 개봉 n일차
        ax2.text(audi_y.iloc[0]['after_release'], 
                audi_y.iloc[0]['acc_audi'],
                f"개봉 {audi_y.iloc[0]['after_release']}일차",
                verticalalignment = 'bottom',
                fontdict={'size':13})
        # 예상 관객수 scatter
        ax2.scatter(audi_y.iloc[0]['after_release'], 
                audi_y.iloc[0]['acc_audi'], 
                marker='*',
                c='yellow',
                linewidth=5, 
                edgecolors='blue',
                zorder=2)
        # 가로 실선
        ax2.axhline(y = audi_x, color='pink', linestyle='--', linewidth=1,zorder=1)
    # 누적 관객수 라인 차트
    lineplot = ax2.plot(df.after_release, df.acc_audi, color='#FF4B4B', linewidth=3,
             label='누적 관객수',zorder=0)
    
    # 서로 다른 축의 범례를 한번에 표시하기
    plots = [barplot]+lineplot
    labels = [l.get_label() for l in plots]
    plt.legend(plots, labels, loc=0)

    # 숫자마다 ,
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
    
    # 누적 관객수(acc_audi)가 예상 관객수(audi_x)보다 높을 때
    if df.iloc[-1]['acc_audi'] >= audi_x: 
        num = df.iloc[-1]['acc_audi'] - audi_x
        delta = f"{format(num, ',')}명"
    else:
        delta = ''

    # 정보를 세 구역을 나눠서 보여주기
    col1, col2, col3= st.columns(3)
    col1.metric(
        label='일일 관객수(명)',
        value=f"{format(df.iloc[-1]['daily_audi'], ',')}",
        delta = f"{format(df.iloc[-1]['daily_audi'] - df.iloc[-2]['daily_audi'],',')}명 (전일 대비)"
    )
    ## 예상 관객수 보다 얼마나 더
    col2.metric(
        label='예상 관객수(명)',
        value=f"{format(audi_x, ',')}"
    )
    col3.metric(
        label=f"개봉 {df.iloc[-1]['after_release']}일차 누적 관객수(명)",
        value=f"{format(df.iloc[-1]['acc_audi'], ',')}",
        delta = delta
    )