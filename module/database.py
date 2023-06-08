import streamlit as st


def db(table):
    # Initialize connection.
    conn = st.experimental_connection('mysql', type='sql')
    
    # Perform query.
    df = conn.query('SELECT * from moredict.'+table+';', ttl=600)

    return df