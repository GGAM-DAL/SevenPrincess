import pandas as pd

# def LoadCsv():
#     df = pd.read_csv('./data/movie_list.csv', encoding='utf-8')
#     return df

# 상영예정작 / 상영작 / 상영종료작끼리 나누어 영화코드 리스트 생성
def CodeList(df, code):
    code_list = []
    # screening = 0:상영예정작 / 1:상영작 / 2:상영종료작
    for i in df[df['screening']==code].index:
        code = df.loc[i, 'code']
        code_list.append(code)
    # 리스트 반환
    return code_list