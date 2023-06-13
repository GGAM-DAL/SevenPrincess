import streamlit as st
import module.logo as Logo

# 완

def Setpage():
    # set page
    st.set_page_config(page_title="The Seven Princesses", 
                       page_icon="princess",
                       initial_sidebar_state="collapsed")
    
    # sidebar disabled
    st.markdown(
    """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>""", unsafe_allow_html=True,)

    # Page Title
    html = Logo.title()
    st.markdown(html, unsafe_allow_html=True,)

def tabs(screening):
    if screening==1:
        menu = ['    ⭐ 평점    ','    🆎 키워드    ','    👥 관객수    ','    ⌨️ 리뷰    ']
    else:
        menu = ['    ⭐ 평점    ','    🆎 키워드    ','    🤔 흥행예측    ','    ⌨️ 리뷰    ']
    css = '''
    <style>
        .stTabs [data-baseweb="tab-list"] {
        font-size:20px;
        text-align:center;
        }
    </style>
    <br>
    '''

    st.markdown(css, unsafe_allow_html=True)
    
    return st.tabs(menu)