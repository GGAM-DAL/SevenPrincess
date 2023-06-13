import streamlit as st
import module.database as Database
import module.page as page
import module.code_list as Codelist
import module.set_page as Setpage


# setting basic page
Setpage.Setpage()

# load data
df = Database.db('movie_info')
code = Codelist.CodeList(df, 1) # Make Code List

page.pages(df, code[3], 1)