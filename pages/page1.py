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
code = Codelist.CodeList(df, 2) # Make Code List



Post.info(df, code[0])  

tabs = Setpage.tabs(1)

with tabs[0]:
    # Show Score
    info.star()
    avg_score = Score.cal_score(code[0])
    Graph.Score(code[0], avg_score)
    
with tabs[1]:
    info.keyword(2)
    center = st.columns((2,1,2))
    emotion = center[1].radio("",('긍정 키워드', '부정 키워드'),
                       horizontal=True)
    if emotion=='긍정 키워드':
        emot = 1
    else:
        emot = 0
    Review.show_review(code[0], emot)
    
with tabs[2]:
    info.audience(2)
    Graph.Audience(code[0], 2)

with tabs[3]:
    info.review()
    Review.review_list(code[0])