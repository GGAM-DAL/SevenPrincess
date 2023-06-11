import streamlit as st
import numpy as np
import module.database as Database

def cal_score(code):
    score_df = Database.db('movie_review')
    score = score_df[score_df.code == code]

    blog_df = score[score.source == 'blog']
    daum_df = score[score.source =='daum']
    lotte_df = score[score.source =='lotte']

    
    # calculate score
    blog = blog_df.star.mean()
    daum = daum_df.star.mean()
    lotte = lotte_df.star.mean()
    num=3
    if np.isnan(blog):
        blog = 0.0
    if np.isnan(daum):
        daum = 0.0
    if np.isnan(lotte):
        lotte = 0.0
    avg_score = score.star.mean()
    
    html=f"""
    <style>
    table, td, th, tr {{text-align:center; border-style: hidden;}}
    </style>
    <table width="100%">
    <tr>
        <th>블로그 평점</th>
        <th>다음 영화 평점</th>
        <th>롯데시네마 평점</th>
        <th>평균 평점</th>
    </tr>
    <tr>
        <td>{blog:.2f}</td>
        <td>{daum:.2f}</td>
        <td>{lotte:.2f}</td>
        <td>{avg_score:.2f}</td>
    </tr>
    </table>
    """

    st.markdown(html, unsafe_allow_html=True)
    return avg_score