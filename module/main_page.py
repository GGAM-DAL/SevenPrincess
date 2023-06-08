import streamlit as st
from streamlit_option_menu import option_menu
import streamlit as st
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

    code = Codelist.CodeList(df, screening) # Make Code List
    st.title(f"You have selected {selected}")

    Post.poster(df, code[0])
    
    # # layout
    # col1, col2 = st.columns(2)
    # with col1:
    #     Post.poster(df, code[0])
    # with col2:
    #     Post.poster(df, code[1])