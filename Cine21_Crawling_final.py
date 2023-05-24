# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# -

service = ChromeService(executable_path = ChromeDriverManager().install())

# # 씨네21 크롤링

## 씨네21 랭킹 페이지 접속
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(3)
url = 'http://www.cine21.com/rank/boxoffice/domestic'
driver.get(url)

## 집계기간 1년 조회
xpath = '//*[@id="data_period"]/a[6]'
driver.find_element(By.XPATH, xpath).click()
xpath = '//*[@id="content"]/div[1]/div/a'
driver.find_element(By.XPATH, xpath).click()


# ## 크롤링을 위한 함수 정의

# ### 컬럼 리스트 추가 함수

def append_li(title, country, genre, date, star, review, director, actor, age,
             release, author, production, distributor):
    title_li.append(title)
    nation_li.append(country)
    genre_li.append(genre)
    date_li.append(date)
    star_li.append(star)
    review_li.append(review)
    director_li.append(director)
    actor_li.append(actor)
    age_li.append(age)
    release_li.append(release)
    author_li.append(author)
    production_li.append(production)
    distributor_li.append(distributor)


# ### 한 페이지에 있는 20개 영화 크롤링 함수
# - 실행하려면 원하는 페이지가 열려 있어야 함

page_source = driver.page_source 
soup = BeautifulSoup(page_source, "html.parser")
info = soup.findAll('p',{'class':'sub_info'})
# if len(info[0].findAll('span')) > 1 :
#     country = info[0].findAll('span')[1].text
# else: country = ''
# genre = info[1].findAll('span')[0].text
# genre
if info[1].findAll('span'):
    genre = info[1].findAll('span')[0].text
else:
    genre = np.nan
genre


def list_crawling(start):
    global title_li, nation_li, genre_li, date_li, star_li, review_li, director_li, actor_li, age_li, release_li, author_li, production_li, distributor_li
    global critic_rating, critic_review, netizen_rating, netizen_review
    title_li = []
    nation_li = []
    genre_li = []
    date_li = []
    star_li = []
    review_li = []
    director_li = []
    actor_li = []
    age_li = []
    release_li = []
    author_li = []
    production_li = []
    distributor_li = []
    
    ## 영화목록 중 영화 들어가기
    lis = driver.find_elements(By.CLASS_NAME, 'boxoffice_li')
    page_source = driver.page_source 
    soup = BeautifulSoup(page_source, "html.parser")
    for d in range(start-1,len(soup.select('.boxoffice_li'))):
        ### 목록 중 정보 없는 영화는 건너 뛰기
        if soup.select('.boxoffice_li')[d].select('div > .nodata'):
            continue
        else:
            ### 영화 클릭
            lis[d].click()
            
            ### 영화 정보 가져오기
            moviepage_source = driver.page_source 
            moviesoup = BeautifulSoup(moviepage_source, "html.parser")
            info = moviesoup.findAll('p',{'class':'sub_info'})
            if len(info[0].findAll('span')) > 1 :
                country = info[0].findAll('span')[1].text
            else: country = np.nan
            if info[1].findAll('span'):
                genre = info[1].findAll('span')[0].text
            else:
                genre = np.nan
            title = moviesoup.find('p', {'class':'tit'}).text
            director = info[3].findAll('a')[0].text
            age = info[0].findAll('span')[-1].text
            release = info[2].findAll('span')[0].text[6:]            
            if len(info) == 4:
                actor = np.nan
            else:
                actor = info[4].findAll('a')[0].text+','+info[4].findAll('a')[1].text
            etcinfo = moviesoup.findAll('ul', {'class':'etcinfo_area'})
            if etcinfo:
                for e in range(len(etcinfo[0].findAll('li'))):
                    if etcinfo[0].findAll('p')[e].text == '각본':
                        author = etcinfo[0].select('li')[e].text.split('\n')[2]
                        break
                    else:
                        author = np.nan
                for e in range(len(etcinfo[0].findAll('li'))):
                    if etcinfo[0].findAll('p')[e].text == '제작':
                        production = etcinfo[0].select('li')[e].text.split('\n')[2]
                        break
                    else:
                        production = np.nan
                for e in range(len(etcinfo[0].findAll('li'))):
                    if etcinfo[0].findAll('p')[e].text == '배급':
                        distributor = etcinfo[0].select('li')[e].text.split('\n')[2]
                        break
                    else:
                        distributor = np.nan
            else:
                author, production, distributor = np.nan, np.nan, np.nan

            ### 리뷰가져오기
            #### 전문가
            critic = moviesoup.find('ul', {'class':'expert_rating'})
            if critic == None:
                append_li(title, country, genre, np.nan, np.nan, np.nan,
                          director, actor, age, release, author, production, distributor)
            else:
                critic_rating = critic.findAll('span', {'class':'num'})
                critic_comment = critic.findAll('span', {'class':'comment'})
                for c in range(len(critic.findAll('li'))): 
                    append_li(title, country, genre, np.nan, critic_rating[c].text, critic_comment[c].text,
                              director, actor, age, release, author, production, distributor)
            #### 네티즌
            pages = moviesoup.select('div.page > a')
            if pages == None:
                append_li(title, country, genre, np.nan, np.nan, np.nan,
                          director, actor, age, release, author, production, distributor)
            else:
                while True:
                    page_source = driver.page_source 
                    reviewsoup = BeautifulSoup(page_source, "html.parser")
                    pages = reviewsoup.select('div.page > a')
                    pages = len(pages)
                    for r in range(2,pages+1):    
                        page_source = driver.page_source 
                        resoup = BeautifulSoup(page_source, "html.parser")
                        netizen = resoup.find('ul', {'class':'reply_box'})
                        for v in range(len(netizen.select('li'))):
                            nz = netizen.select('li')[v]        
                            netizen_rating = nz.findAll('span', {'class':'num'})
                            netizen_date = nz.findAll('div', {'class':'date'})
                            netizen_comment1 = nz.findAll('div', {'class':'comment'})
                            if netizen_comment1:
                                append_li(title, country, genre, netizen_date[0].text, critic_rating[0].text, netizen_comment1[0].text,
                                      director, actor, age, release, author, production, distributor)

                            else:
                                netizen_comment2 = nz.findAll('div', {'class':'comment ellipsis_3'})
                                append_li(title, country, genre, netizen_date[0].text, critic_rating[0].text, netizen_comment2[0].text,
                                      director, actor, age, release, author, production, distributor)
                        driver.implicitly_wait(25)
                        time.sleep(3)
                        xpath = '//*[@id="netizen_review_area"]/div/div/a['+str(r)+']'
                        driver.find_element(By.XPATH, xpath).click()
                        driver.implicitly_wait(25)
                        time.sleep(2)
                    if reviewsoup.select('.pagination > .btn_next'):
                        pagination = driver.find_element(By.CLASS_NAME, 'pagination')
                        pagination.find_element(By.CLASS_NAME, 'btn_next').click()
                        time.sleep(3)
                        driver.implicitly_wait(25)
                    else:
                        break
            ### 뒤로가기(목록으로 돌아가기)
            driver.back()
            time.sleep(3)
    driver.implicitly_wait(10)
    ## 1년 조회 재설정
    xpath = '//*[@id="data_period"]/a[6]'
    driver.find_element(By.XPATH, xpath).click()
    driver.implicitly_wait(5)
    xpath = '//*[@id="content"]/div[1]/div/a'
    driver.find_element(By.XPATH, xpath).click()    
    time.sleep(5)


# ### 페이지 리스트 내 모든 영화 가져오기
# - 실행하려면 원하는 시작페이지가 열려있어야 함
# - total_list_crawling(원하는 시작페이지 셋, 시작페이지셋 안에 시작페이지 번호)

def total_list_crawling(startpage=1, startlistnum=1):
    global title_li, nation_li, genre_li, date_li, star_li, review_li, director_li, actor_li, age_li, release_li, author_li, production_li, distributor_li    
    global df
    title_li = []
    nation_li = []
    genre_li = []
    date_li = []
    star_li = []
    review_li = []
    director_li = []
    actor_li = []
    age_li = []
    release_li = []
    author_li = []
    production_li = []
    distributor_li = []
    df = pd.DataFrame({'title':title_li, 'nation':nation_li, 'genre':genre_li,
                          'review':review_li, 'star':star_li, 'date':date_li,
                          'director':director_li, 'actor':actor_li, 'release':release_li,
                          'age':age_li, 'author':author_li, 'production':production_li,
                          'distributor':distributor_li})
    # 랭킹 페이지 목록
    page_source = driver.page_source 
    soup = BeautifulSoup(page_source, "html.parser")
    pages = soup.select('div.page > a')
    pages = len(pages)
    for p in range(startlistnum, pages+1):
        ## 현재 페이지 내 영화 전체 크롤링
        list_crawling(1) ### -> 1년 조회로 초기화된 상태
        df2 = pd.DataFrame({'title':title_li, 'nation':nation_li, 'genre':genre_li,
                          'review':review_li, 'star':star_li, 'date':date_li,
                          'director':director_li, 'actor':actor_li, 'release':release_li,
                          'age':age_li, 'author':author_li, 'production':production_li,
                          'distributor':distributor_li})
        df = pd.concat([df, df2])
        ### 마지막 페이지에서 종료
        if p == pages:
            break
        else:
            ### 원하는 페이지셋까지 '다음' 버튼 눌러줘야 함
            for _ in range(startpage-1):
                driver.find_element(By.CLASS_NAME, 'btn_next').click()
                time.sleep(3)
                driver.implicitly_wait(10)
            ### 다음 페이지 숫자 버튼 누르기
            xpath = '//*[@id="boxoffice_list_content"]/div/div/a['+str(p+1)+']'
            driver.find_element(By.XPATH, xpath).click()
        time.sleep(3)
    return df


review_df = total_list_crawling(22,8)

review_df

review_df = pd.DataFrame({'title':title_li, 'nation':nation_li, 'genre':genre_li,
                          'review':review_li, 'star':star_li, 'date':date_li,
                          'director':director_li, 'actor':actor_li, 'release':release_li,
                          'age':age_li, 'author':author_li, 'production':production_li,
                          'distributor':distributor_li})
review_df

little = df
little

## total
review_df2 = pd.concat([review_df2, little])
review_df2

review_df2.to_csv('cine21_review_230520.csv', encoding='utf-8')

# ## 데이터 전처리
# - 중복 제거
# - 컬럼에 잘못 들어간거 결측치 처리

review_df2 = pd.read_csv('cine21_review_230520.csv', index_col=0)
review_df2

# #### \n, \t 문자열 제거

review_df2["review"] = review_df2["review"].str.replace('\n','', regex=True)
review_df2["review"] = review_df2["review"].str.replace('\t','', regex=True)
review_df2

# #### 중복행 제거

review = review_df2.drop_duplicates(['title','review'])
review

# - 인덱스 reset

review.reset_index(drop=True, inplace=True)

# #### nation 열에서 15세관람가, 전체관람가 결측치 처리

review.nation.unique()

for i in range(len(review)):
    if ((review['nation'][i] == '15세이상관람가')|((review['nation'][i] == '전체 관람가')|(review['nation'][i] == '')):
        review['nation'][i] = np.nan

review.nation.unique()

# #### genre열에서 상영시간 결측치 처리

review.genre.unique()

for i in range(len(review)):
    if type(review['genre'][i]) == float:
        continue
    elif review['genre'][i][-1] == '분':
        review['genre'][i] = np.nan

review.genre.unique()

# #### release열에서 관람객 결측치 처리

review.release.unique()

for i in range(len(review)):
    if type(review['release'][i]) == float:
        continue
    elif review['release'][i][-1] == '명':
        review['release'][i] = np.nan

review.release.unique()

# #### age열에서 상영등급만 남기고 결측치 처리

review.age.unique()

review['age'][4740] in ['청소년 관람불가', '12세이상관람가', '15세이상관람가', '전체 관람가']

for i in range(len(review)):
    if review['age'][i] in ['청소년 관람불가', '12세이상관람가', '15세이상관람가', '전체 관람가']:
        continue
    else:
        review['age'][i] = np.nan

review.age.unique()

# ## 데이터 내보내기

review.to_csv('cine21_review.csv', encoding='utf-8')
