import streamlit as st
import numpy as np
import module.database as Database

def style_metric_cards(background_color: str = "#FFF",
    border_size_px: int = 1,
    border_color: str = "#CCC",
    border_radius_px: int = 5,
    border_left_color: str = "#800080",
    box_shadow: bool = False,):

    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            div[data-testid="metric-container"] {{
                text-align:center;
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                {box_shadow_str}

            }}
            label [data-testid="metric-container"] {{
                width: fit-content;
                margin: auto;
            }}
        </style>
        """,
        unsafe_allow_html=True,
)

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

    if np.isnan(blog):
        blog = 0.0
    if np.isnan(daum):
        daum = 0.0
    if np.isnan(lotte):
        lotte = 0.0
    avg_score = score.star.mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        label='네이버 블로그 평점',
        value=f"{blog:.2f}"
    )    
    c2.metric(
        label='다음 영화 평점',
        value=f"{daum:.2f}"
    )    
    c3.metric(
        label='롯데시네마 평점',
        value=f"{lotte:.2f}"
    )    
    c4.metric(
        label='평균 평점',
        value=f"{avg_score:.2f}"
    )
    style_metric_cards()

    return avg_score