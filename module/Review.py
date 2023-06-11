import plotly.graph_objects as px
import streamlit as st
import numpy as np
import module.database as Database

# 완

step = 0
def show_review(code, emotion):
    df = Database.db('movie_info')
    df = df[df['code']==code]
    if df.iloc[0]['screening'] == 0:
        html="<h1 style='text-align:center;'>Before Release</h1>"
        st.markdown(html, unsafe_allow_html=True)
        return

    neg_pos = ['부정','긍정']
    html = f"""
    <style>
        .expander {{
            text-align: center;
            font-weight: bold;
            font-size: 23px;
            padding-top: 20px;
        }}
        .key {{color: pink;}}
    </style>
    <div class="expander">{neg_pos[emotion]} <span class="key">Key!</span>word
    </div>"""
    
    

    keyword_df = Database.db('keyword_review')
    keyword = keyword_df[keyword_df['code'] == code]
    emot = keyword[keyword['emotion']==emotion].reset_index(drop=True)

    st.markdown(html, unsafe_allow_html=True)
    keyword_l = list(emot.keyword.unique())
    for i,k in enumerate(keyword_l):
        df = emot[emot['keyword']==k].reset_index(drop=True)
        with st.expander(f"Ranking {i+1}! {k}"):
            for key in df['review']:
                st.write('▶ ', key)
    st.markdown('<br><br>', unsafe_allow_html=True)
    key1, key2 = st.columns(2)
    
    # 파이차트
    key2.markdown(f'<h5><center>Top 5 {neg_pos[emotion]} 키워드 파이차트</center></h5>',unsafe_allow_html=True)
    colors = ['#C6DBDA','#FEE1E8','#FED7C3','#F6EAC2','#ECD5E3']
    pie = emot.drop_duplicates(subset='keyword')
    fig = px.Figure(data=[px.Pie(labels=pie.keyword,
                                 values=np.round(pie.score,2), 
                                 hole=.5)])
    fig.update_traces(hoverinfo='percent', textinfo='label+value',
                      textfont_size=13, marker=dict(colors=colors))
    fig.update_layout(margin=dict(l=20, r=20, t=0, b=0),)
    key2.markdown('<p style="color: gray; font-size:5px; text-aligh: left; margin-top: 0px;">연관성, 빈도, 유사도를 바탕을 측정된 점수입니다.</p>', unsafe_allow_html=True)
    key2.plotly_chart(fig, use_container_width=True)
    

    # 워드 클라우드
    df = Database.db('word_cloud')
    df = df[(df['code']==code)&(df['emotion']==emotion)]
    html = f"""
    <div>
        <img src="{df.iloc[0]['word_cloud']}" alt="word cloud" style='width: 100%'>
    </div>
    """
    key1.markdown(f'<h5><center>{neg_pos[emotion]} 리뷰 워드 클라우드</center></h5>',unsafe_allow_html=True)
    key1.markdown(html, unsafe_allow_html=True)

    
def review_list(code):
    global step

    review = Database.db('movie_review')
    center = st.columns([1,4,1])
    # review = review[review['source']=='blog']
    select = center[1].radio("",('최신순', '오래된순', '높은 평점순', '낮은 평점순'),
                       horizontal=True)
    if select == '최신순':
        col = 'after_release'
        bool = False
    elif select == '오래된순':
        col = 'after_release'
        bool = True
    elif select == '높은 평점순':
        col = 'star'
        bool = False
    elif select == '낮은 평점순':
        col = 'star'
        bool = True
    df = review[review['code']==code]
    df.sort_values(col, ascending=bool, inplace=True)
    df.reset_index(drop=True, inplace=True)
    # 버튼 기본식이 단순함
    # 
    len = df.shape[0]
    if len < 10:
        step_e = len
    else:
        step_e = 10
    center = st.columns([1,1,1,1,1,1,1])

    with center[1]:
        if st.button('<<'):
            step = 0
            step_e = step+10
    with center[2]:
        if st.button('<'):
            if step != 0:
                step -= 10
                step_e = step+10
    with center[4]:
        if st.button('\>'):
            step += 10
            if step > len:
                step = len // 10 * 10
                step_e = step+len % 10
            step_e = step+10
    with center[5]:
        if st.button('\>>'):
            step = len // 10 * 10
            step_e = step+len % 10
    with center[3]:
        st.write(step//10 + 1,'페이지 / ', len//10 + 1,'페이지')

    
    for i in range(step, step_e):
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
</style>
<body>
    <div class='box'>
        <div class='review'>
            <p>🌟{df.iloc[i]['star']}</p>
            <p>{df.iloc[i]['review']}</p>
            <p>{df.iloc[i]['source']}<span style="white-space:pre;">&#9;</span>{df.iloc[i]['date']}</p>
        </div>
    </div>

</body>
    """
        st.markdown(html, unsafe_allow_html=True)
    
