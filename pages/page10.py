import streamlit as st
import module.database as Database
import module.Poster as Post
import module.Graph as Graph
import module.code_list as Codelist
import module.set_page as Setpage
import module.Review as Review
import module.Score as Score
import module.Graph as Graph
import module.information as info
import pandas as pd

# setting basic page
Setpage.Setpage()

# load data
df = Database.db('movie_info')
code = Codelist.CodeList(df, 2) # Make Code List



Post.info(df, code[4])  


tab1, tab2, tab3, tab4 = st.tabs(['평점','키워드','관객수','리뷰'])

with tab1:
    # Show Score
    info.star()
    avg_score = Score.cal_score(code[4])
    Graph.Score(code[4], avg_score)
with tab2:
    info.keyword(2)
    emotion = st.radio("선택",('긍정 키워드', '부정 키워드'),
                       horizontal=True)
    if emotion=='긍정 키워드':
        emot = 1
    else:
        emot = 0
    Review.show_review(code[4], emot)
    
with tab3:
    info.audience(2)
    Graph.Audience(code[4], 2)
with tab4:
    info.review()
    Review.review_list(code[4])