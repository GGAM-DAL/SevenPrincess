import pandas as pd

def LoadCsv():
    df = pd.read_csv('./data/movie_list.csv', encoding='utf-8')
    return df

def CodeList(df, code):
    code_list = []
    for i in df[df['screening']==code].index:
        code = df.loc[i, 'code']
        code_list.append(code)
    return code_list