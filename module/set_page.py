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