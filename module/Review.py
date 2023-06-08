import pandas as pd
import streamlit as st
import module.database as Database

# 완

def dict_review(code):
    pos_df = Database.db('pos_keyword')
    pos = pos_df[pos_df['code'] == code].reset_index(drop=True).to_dict()
    
    neg_df = Database.db('neg_keyword')
    neg = neg_df[neg_df['code'] == code].reset_index(drop=True).to_dict()
    
    return pos, neg
    
def show_review(pos, neg):
    key1, key2 = st.columns(2)

    html1 = """
    <style>
        .expander {
            text-align: center;
            font-weight: bold;
            font-size: 23px;
            padding-top: 20px;
        }
        .key {color: pink;}
    </style>
    <div class="expander">
        Positive <span class="key">Key!</span>word
    </div>"""
    html2 = """
    <div class="expander">
        Negative <span class="key">Key!</span>word
    </div>"""
    
    key1.markdown(html1, unsafe_allow_html=True)
    for i in [0,1,2]:
        with key1.expander(f"Ranking {pos['ranking'][i]}! {pos['keyword'][i]}"):
            for key in ['review1','review2','review3','review4','review5']:
                st.write(': ', pos[key][i])
    
    key2.markdown(html2, unsafe_allow_html=True)
    for i in [0,1,2]:
        with key2.expander(f"Ranking {neg['ranking'][i]}! {neg['keyword'][i]}"):
            for key in ['review1','review2','review3','review4','review5']:
                st.write(': ', neg[key][i])