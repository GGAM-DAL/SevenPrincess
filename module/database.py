import streamlit as st
# mysql 연동을 위한 설치 패키지
import flask_sqlalchemy
# import mysqlclient
# pip install flask_sqlalchemy
# pip install mysqlclient -> 이거 스트림릿에 설치 에러나서 pymysql 설치함 ;;

def db(table):
    # Initialize connection.
    conn = st.experimental_connection('mysql', type='sql')
    
    # Perform query.
    df = conn.query('SELECT * from moredictdb.'+table+';', ttl=600)

    return df
