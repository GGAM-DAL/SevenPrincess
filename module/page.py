import streamlit as st
import module.Poster as Post
import module.Graph as Graph
import module.set_page as Setpage
import module.Review as Review
import module.Score as Score
import module.Graph as Graph
import module.information as info


def pages(df, code, screening):
    # Disply Movie Poster & Information
    Post.info(df, code)  

    # Make tabs
    tabs = Setpage.tabs(1)

    # tab1 : Show score
    with tabs[0]:
        # Show Score Information
        info.star()
        # Show site star & Calculate avarage score
        avg_score = Score.cal_score(code)
        # Show score line chart & socre histogram
        Graph.Score(code, avg_score)

    # tab2 : Show Keyword & Review & WordCloud
    with tabs[1]:
        # Show Information
        info.keyword()
        # Make Radio Button
        emotion = st.radio("",('긍정 키워드', '부정 키워드'),
                       horizontal=True)
        # Make emot
        if emotion=='긍정 키워드':
            emot = 1
        else:
            emot = 0

            """
        keyword list
        neg_pos[0] : 부정
        neg_pos[1] : 긍정
        """
        neg_pos = ['부정','긍정']
        
        # Show Keyword Review & Word Cloud
        Review.show_keyword_review(code, emot, neg_pos[emot])
        Review.show_wordcloud(code, emot, neg_pos[emot])

    # tab3 : Show Audience Information
    with tabs[2]:
        # Show Information
        info.audience(screening)
        # Show Audience Graph & Information
        Graph.Audience(code, screening)

    # tab4 : All site reviw
    with tabs[3]:
        # Show Information
        info.review()
        # Show site review
        Review.review_list(code)