import streamlit as st

def keyword(screening):
    st.markdown('<h3><center>긍/부정 키워드를 통한 리뷰 확인하기</center></h3>',unsafe_allow_html=True)
    if screening == 0:
        html = """
        <h4>영화가 개봉하면 확인해주세요</h4>
        """
        st.markdown(html, unsafe_allow_html=True)
        
    html = """
        <p>🎥 높은/낮은 평점에서 차지하는 키워드 Top 5!</p>
        <p>🎥 긍정 키워드는 평점이 높은 순으로, 부정 키워드는 평점이 낮은 순으로 정렬했습니다</p>
        <p>🎥 각 키워드 옆 아래 화살표를 클릭하면 키워드가 포함된 실제 리뷰를 확인하실 수 있습니다!</p>
        <p>🎥 파이차트에 그려진 5개의 단어는 다음영화, 롯데시네마 리뷰데이터를 바탕으로 추출된 긍정리뷰에 대한 TOP5 키워드입니다.</p>
    """
    st.markdown(html, unsafe_allow_html=True)

def audience(screening):
    st.markdown('<h3><center>개봉 후 관객수 그래프</center></h3>',unsafe_allow_html=True)
    if screening == 0:
        html = """
        <h4>영화가 개봉하면 확인해주세요</h4>
        """
        st.markdown(html, unsafe_allow_html=True)
        
    html = """
        <p>🎥 개봉 후 누적 관객수를 선 그래프로 보여줍니다.</p>
        <p>🎥 개봉 후 일일 관객수를 막대 그래프로 보여줍니다.</p>
    """
    st.markdown(html, unsafe_allow_html=True)

def star():
    st.markdown('<h3><center>사이트 별 평점</center></h3>',unsafe_allow_html=True)
    html = """
        <p>🎥 사이트별 평점과 평점의 분포 그리고 평균 평점을 확인하실 수 있습니다!</p>
        <p>🎥 daum - 영화 사이트 '다음 영화'에서 기재된 평점</p>
        <p>🎥 lotte - 영화 예매 사이트 '롯데시네마'에서 기재된 평점</p>
        <p>🎥 blog - 네이버 블로그에 게시된 영화 후기를 수집하여 요약 후 평점 예측 모델을 통해 얻은 평점</p>
    """
    st.markdown(html, unsafe_allow_html=True)
def review():
    st.markdown('<h3><center>영화 관람객 작성 리뷰</center></h3>',unsafe_allow_html=True)

    html = """
        <p>🎥 daum - 영화 사이트 '다음 영화'에서 작성된 리뷰</p>
        <p>🎥 lotte - 영화 예매 사이트 '롯데시네마'에서 작성된 리뷰</p>
        <p>🎥 blog - 네이버 블로그에 게시된 영화 후기를 수집하여 요약 후 평점 예측 모델을 통해 얻은 리뷰와 평점</p>
    """
    st.markdown(html, unsafe_allow_html=True)