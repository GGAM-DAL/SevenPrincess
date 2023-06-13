import streamlit as st
import module.information as info
import module.database as Database

# globale variable step
step = 0

def show_keyword_review(code, emotion, neg_pos):
    df = Database.db('movie_info')
    df = df[df['code']==code]

    # before release
    if df.iloc[0]['screening'] == 0:
        html="<h1 style='text-align:center;'>😉 개봉 후 확인해주세요</h1>"
        st.markdown(html, unsafe_allow_html=True)

        return

    # show title
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
    <div class="expander">{neg_pos} <span class="key">Key!</span>word
    </div>"""
    st.markdown(html, unsafe_allow_html=True)
    
    # show keyword reviews
    keyword_df = Database.db('keyword_review')
    keyword = keyword_df[keyword_df['code'] == code]

    # positive / negative reviews dataframe
    emot = keyword[keyword['emotion']==emotion].reset_index(drop=True)
    # keywords list
    keyword_l = list(emot.keyword.unique())

    # show keywords & reviews
    for i,k in enumerate(keyword_l):
        # one keyword
        df = emot[emot['keyword']==k].reset_index(drop=True)
        # show reviews
        with st.expander(f"Ranking {i+1}! {k}"):
            for key in df['review']:
                st.write('▶ ', key)
    st.markdown('<br><br>', unsafe_allow_html=True)

def show_wordcloud(code, emotion, neg_pos):
    df = Database.db('movie_info')
    df = df[df['code']==code]

    if df.iloc[0]['screening'] == 0:
        return
    # show word cloud
    df = Database.db('word_cloud')
    df = df[(df['code']==code)&(df['emotion']==emotion)]
    html = f"""
    <style>
        .wordcloud {{
        text-align:center;
        }}
    </style>
    <div class='wordcloud'>
        <img src="{df.iloc[0]['word_cloud']}" alt="word cloud" style='width: 500px'>
    </div>
    """
    # wordcloud information
    info.hovers(f'리뷰 워드 클라우드', neg_pos)
    st.markdown(html, unsafe_allow_html=True)


# show all reviews
def review_list(code):
    # use global variable 'step' - dtype is 'int' 
    global step

    # Make dataframe
    review = Database.db('movie_review')
    df = review[review['code']==code]

    center = st.columns([1,4,1])
    # review = review[review['source']=='blog']

    # Make Radio Button
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

    # dataframe sorting
    df.sort_values(col, ascending=bool, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # dataframe length
    len = df.shape[0]

    if len < 10:
        # end step value : range( , step_e)
        step_e = len
    else:
        step_e = 10

    # make button
    center = st.columns([1,1,1,1,1,1,1])
    # first page
    with center[1]:
        if st.button('<<'):
            step = 0
            step_e = step+10
    # previous page
    with center[2]:
        if st.button('<'):
            if step != 0:
                step -= 10
                step_e = step+10
    # next page
    with center[4]:
        if st.button('\>'):
            step += 10
            if step > len:
                step = len // 10 * 10
                step_e = step+len % 10
            step_e = step+10
    # last page
    with center[5]:
        if st.button('\>>'):
            step = len // 10 * 10
            step_e = step+len % 10
    # show current page
    with center[3]:
        st.write(step//10 + 1,'페이지 / ', len//10 + 1,'페이지')

    
    # show review
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
    
