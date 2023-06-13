import streamlit as st

def keyword():
    st.markdown('<h3><center>긍/부정 키워드를 통한 리뷰 확인하기</center></h3>',unsafe_allow_html=True)
        
    html = """
        <style>
            .keyword {
                font-size: 13px;
            }
        </style>
        <p>🎥 긍정/부정 리뷰에서 뽑은 키워드 Top 5!</p>
        <p class="keyword">&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 각 긍정 키워드에 보여지는 리뷰들은 높은 평점순으로 보여집니다</p>
        <p class="keyword">&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 각 부정 키워드에 보여지는 리뷰들은 낮은 평점순으로 보여집니다</p>
        <p class="keyword">&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 각 키워드 탭을 클릭하여 키워드가 포함된 실제 리뷰를 확인하실 수 있습니다!</p>
        <br>
    """
    st.markdown(html, unsafe_allow_html=True)

def audience(screening):
    
    if screening == 0:
        st.markdown('<h3><center>영화 흥행 예측</center></h3>',unsafe_allow_html=True)
        html_s = """
            <style>
                .h {
                    font-size: 13px;
                }
            </style>
            <p>🎥 영화 흥행 예측 영화 기본 정보(장르, 배급사, 상영등급 등)를 분석하여 영화의 흥행 수준을 예측합니다.</p>
            <p class='h'>&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 미흥행 : 최종 관람객 수 50만 미만 예상</p>
            <p class='h'>&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 흥행 : 최종 관람객 수 50만 이상 500만 미만 예상</p>
            <p class='h'>&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 대흥행 : 최종 관람객 수 500만 이상 예상</p>
            <br>
        """
        st.markdown(html_s, unsafe_allow_html=True)
        return
    st.markdown('<h3><center>개봉 후 관객수 그래프</center></h3>',unsafe_allow_html=True)
    html = """
        <style>
            .audi {
                font-size: 13px;
            }
        </style>
        <p> 🎥 개봉된 영화의 관객수 정보를 보여줍니다.</p>
        <p> 🎥 개봉 1주차 관객수 정보가 모이면 예상관객수를 예측해 정보를 제공합니다.</p>
        <p class='audi'>&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 그래프의 왼쪽 y축은 개봉 후 일일 관객수를 나타냅니다.</p>
        <p class='audi'>&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 그래프의 오른쪽 y축은 개봉 후 누적 관객수를 나타냅니다.</p>
        <br><br>
    """
    st.markdown(html, unsafe_allow_html=True)

def star():
    st.markdown('<h3><center>사이트 별 평점</center></h3>',unsafe_allow_html=True)

    html = """
        <style>
            .star {
                font-size: 13px;
            }
        </style>
        <p>🎥 사이트별 평점과 평점의 분포 그리고 평균 평점을 확인하실 수 있습니다!</p>
        <p class='star'>&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 daum - 영화 사이트 '다음 영화'에서 기재된 평점</p>
        <p class='star'>&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 lotte - 영화 예매 사이트 '롯데시네마'에서 기재된 평점</p>
        <p class='star'>&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 blog - 네이버 블로그에 게시된 영화 후기를 수집하여 요약 후 평점 예측 모델을 통해 얻은 평점</p>
        <br><br>
    """
    st.markdown(html, unsafe_allow_html=True)
def review():
    st.markdown('<h3><center>영화 관람객 작성 리뷰</center></h3>',unsafe_allow_html=True)

    html = """
        <style>
            .hi {
                font-size: 13px;
            }
        </style>
        <p>🎥 모든 사이트의 리뷰를 한번에 확인하실 수 있습니다!</p>
        <p class='hi'>&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 daum - 영화 사이트 '다음 영화'에서 작성된 리뷰</p>
        <p class='hi'>&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 lotte - 영화 예매 사이트 '롯데시네마'에서 작성된 리뷰</p>
        <p class='hi'>&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;🎥 blog - 네이버 블로그에 게시된 영화 후기를 수집하여 요약 후 평점 예측 모델을 통해 얻은 리뷰와 평점</p>
    """
    st.markdown(html, unsafe_allow_html=True)


def hovers(title, emot):
    hover = f"""
    <style>
.tooltip {{
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black;
}}

.tooltip .tooltiptext {{
  visibility: hidden;
  width: 300px;
  background-color: black;
  color: #fff;
  text-align: left;
  border-radius: 6px;
  padding: 5px 0;
  position: absolute;
  z-index: 1;
  top: -5px;
  left: 110%;
}}

.tooltip .tooltiptext::after {{
  content: "";
  position: absolute;
  top: 50%;
  right: 100%;
  margin-top: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: transparent black transparent transparent;
}}
.tooltip:hover .tooltiptext {{
  visibility: visible;
}}
</style>
<body style="text-align:center;">
<h5><center>{emot} {title}<span class="tooltip"> ❓
    <p class="tooltiptext"> 🎥 {emot} 리뷰에서 추출한 키워드 100개 중 명사를 기준으로 언급량에 따른 워드클라우드</p></span>
</center></h5>

</body>
    """
    st.markdown(hover, unsafe_allow_html=True)