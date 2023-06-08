import streamlit as st
import module.Poster as Post
import module.code_list as Codelist
import module.set_page as Setpage
import module.Keyword as Keyword
import module.Review as Review
import module.Score as Score
import pandas as pd

# setting basic page
Setpage.Setpage()

# load data
df = Codelist.LoadCsv()
code = Codelist.CodeList(df, 2) # Make Code List

col1, col2, col3 = st.columns([1,2,3])

with col1:
    Post.info(df, code[1])  
           
with col2:
    Score.cal_score(code[1])

    # Review List
    p_list, n_list = Review.review(code[1])
    # Keyword Expander
    Keyword.keyword(p_list, n_list)

with col3:
    Score.score(code[1])
    Score.score(code[1])