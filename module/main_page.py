import streamlit as st
from streamlit_option_menu import option_menu
import module.code_list as Codelist
import module.Poster as Post

## 이제 수정할 것 없음 ##

class nav():
    def streamlit_menu(example):
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["상영예정작", "상영작", "상영종료작"],  # required
            icons=["camera-reels", "film", "camera-video-off"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            )
        return selected
    
def Mainpage(df, selected):
    if selected == "상영예정작":
        screening = 0
    elif selected == "상영작":
        screening = 1
    else:
        screening = 2
    if screening == 0:
        df.loc[10] = [11, '분노의 질주: 라이드 오어 다이','#','#','#','#',0,'https://t1.daumcdn.net/movie/6fed61e73b455aba36c3c4b434b6fafe2944e698']
        df.loc[11] = [12, '말없는 소녀','#','#','#','#',0,'https://t1.daumcdn.net/movie/3cdc596cb0d48c05d2210f7ebadab55587c0e179']
        df.loc[12] = [13, '트랜스포머: 비스트의 서막','#','#','#','#',0,'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/yqXbE4epcDgxJd89hhqNXiNYjMc.jpg']
    code = Codelist.CodeList(df, screening) # Make Code List

    length = len(code)
    # layout
    col1, col2 = st.columns(2)
    with col1:
        Post.poster(df, code[0])
    if length > 1:
        with col2:
            Post.poster(df, code[1])
    if length>2:
        col3, col4 = st.columns(2)
        with col3:
            Post.poster(df, code[2])
        with col4:
            Post.poster(df, code[3])
    if length > 4:
        col5, col6 = st.columns(2)
        with col5:
            Post.poster(df, code[4])
    if length > 5:
        with col6:
            Post.poster(df, code[5])
