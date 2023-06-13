import streamlit as st
import module.database as Database
import module.Poster as Post
import module.Graph as Graph
import module.code_list as Codelist
import module.set_page as Setpage
import module.Review as Review
import module.Score as Score
import module.Graph as Graph
import pandas as pd
import module.information as info

# setting basic page
Setpage.Setpage()

# load data
df = Database.db('movie_info')
code = Codelist.CodeList(df, 0) # Make Code List



Post.info(df, code[0])  


tabs = Setpage.tabs(0)
# 흥행 기준 설명
# 카드로 작성
with tabs[0]:
    # Show Score
    info.star()
    avg_score = Score.cal_score(code[0])
    Graph.Score(code[0], avg_score)
with tabs[1]:
    info.keyword(0)
    emotion = st.radio("",('긍정 키워드', '부정 키워드'),
                       horizontal=True)
    if emotion=='긍정 키워드':
        emot = 1
    else:
        emot = 0
    Review.show_review(code[0], emot)
    
with tabs[2]:
    info.audience(0)
    Graph.Audience(code[0], 0)
with tabs[3]:
    info.review()
    Review.review_list(code[0])