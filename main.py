import streamlit as st
import module.main_page as Mainpage
import module.database as Database
import module.set_page as Setpage
# from flask_sqlalchemy import SQLAlchemy

# Setting basic page
Setpage.Setpage()

# Load Database Table 'movie'
movie = Database.db('movie')

# Navigation bar
selected = Mainpage.nav().streamlit_menu()

# Main page
Mainpage.Mainpage(movie, selected)