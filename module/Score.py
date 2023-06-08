import streamlit as st
import numpy as np
import module.database as Database

def cal_score(code):
    score_df = Database.db('review_info')
    score = score_df[score_df.code == code]

    blog_df = score[score.source == 'blog']
    site_df = score[score.source !='blog']

    # calculate score
    blog = blog_df.star.mean()
    site = site_df.star.mean()
    if np.isnan(blog):
        blog = 0.0
        num = 1
    if np.isnan(site):
        site = 0.0
        num = 1
    avg_score = (blog + site) / num
    
    html=f"""
        <style>
            .table {{
                width:100%;
                border-collapse: separate !important;
                -moz-border-radius: 10px;
                -webkit-border-radius: 10px;
                border-radius: 10px;
            }}
            .row {{
                border-style: hidden;
                text-align: center;
                font-weight: bold;
            }}
            .score1 {{
                font-size:20px;
                border-collapse: separate !important;
                border: 1px solid #444444;
                -moz-border-radius: 10px;
                -webkit-border-radius: 10px;
                border-radius: 10px;}}
            .score2 {{
                font-size:26px; 
                background-color: pink;
                border-collapse: separate !important;
                border: 1px solid #444444;
                -moz-border-radius: 10px;
                -webkit-border-radius: 10px;
                border-radius: 10px;}}
        </style>
        <table class="table">
            <tr class="row">
                <td class="score1">블로그 평점 : {blog:.2f}</td>
                <td class="score2">평점</td>
            </tr>
            <tr class="row">
                <td class="score1">사이트 평점 : {site:.2f}</td>
                <td class="score2">{avg_score:.2f}</td>
            </tr>
        </table>
    """
    st.markdown(html, unsafe_allow_html=True)