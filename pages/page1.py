import streamlit as st
import module.database as Database
import module.Poster as Post
import module.code_list as Codelist
import module.set_page as Setpage
import module.Review as Review
import module.Score as Score
import module.Graph as Graph
import pandas as pd

# setting basic page
Setpage.Setpage()

# load data
df = Database.db('movie')
code = Codelist.CodeList(df, 2) # Make Code List

col1, col2, col3 = st.columns([1,2.5,3])

with col1:
    Post.info(df, code[0])  
           
with col2:
    # Show Score
    Score.cal_score(code[0])

    # Review dictionary
    pos, neg = Review.dict_review(code[0])

    # Show Keyword Review
    Review.show_review(pos, neg)

with col3:
    Graph.Audience(code[0], 2)