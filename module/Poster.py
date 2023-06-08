import streamlit as st

# 완

def poster(df, code):
    dict = df[df['code']==code].reset_index(drop=True).to_dict()
    html=f"""
        <div style="text-align: center;">
        <a href="http://localhost:8501/page{dict['code'][0]}" target="_self">
            <img src="{dict['img_url'][0]}" alt="poster" style='width: 200px;'>
        </a>
        </div>
    """
    st.markdown(html, unsafe_allow_html=True,)
    st.markdown(f"<div style='text-align: center; margin-top: 10px'>{dict['title'][0]}</div>",
                 unsafe_allow_html=True,)

def info(df, code):
    dict = df[df['code']==code].reset_index(drop=True).to_dict()
    html=f"""
    <head>
        <style>
            .info {{
                border-style: hidden;
            }}
            .hit {{
                text-align: center;
                color: white;
                background-color: #b0cddf;
                font-size: 2rem;
                border-collapse: separate !important;
                -moz-border-radius: 10px;
                -webkit-border-radius: 10px;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <!--영화 정보 테이블 => 왼쪽 고정-->
        <div style="text-align: left; position:fixed;"> 
            <table class="info" height="250px" style="font-weight: bold;">
                <tr class="info" >
                    <td colspan="2" height="300px" style="border-style: hidden;">
                        <!--포스터-->
                        <img src={dict['img_url'][0]} alt="poster" style='width: 200px; position:absolute; top:0px;'>
                        <!--흥행도장-->
                        <img style="position:relative;transform:rotate(-45deg);" src="https://github.com/GGAM-DAL/SevenPrincess/blob/GGAM-DAL/static/대흥행.png?raw=true">
                    </td>
                </tr>
                <tr class="info" >
                    <th colspan="2" style="font-size: 26px;">{dict['title'][0]}</th>
                </tr>
                <tr class="info" >
                    <td width="85">장르</td>
                    <td width="115">{dict['genre'][0]}</td>
                </tr>
                <tr class="info" >
                    <td>개봉일</td>
                    <td>{dict['date'][0]}</td>
                </tr>
                <tr class="info" >
                    <td>감독</td>
                    <td>{dict['director'][0]}</td>
                </tr>
                <tr class="info" >
                    <td>출연 배우</td>
                    <td style="font-size:1;">{dict['actor'][0]}</td>
                </tr>
            </table>
        </div>
    </body>
    """
    st.markdown(html, unsafe_allow_html=True)
