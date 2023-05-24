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

from textrank import KeysentenceSummarizer
from textrank import KeywordSummarizer
import re
import numpy as np
from kss import split_sentences
from konlpy.tag import Komoran, Okt, Kkma

f = open('stopwords-ko.txt','r', encoding='utf-8')
stopwords = f.read().splitlines()
stopwords


# +
def komoran_tokenizer(sent):
    komoran = Komoran()
    words = komoran.pos(sent, join=True)
    words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
    return words

def komoran_tokenize(sent):
    words = sent.split()
    words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
    return words

def okt_tokenizer(sent):
    okt = Okt()
    words = okt.pos(sent, norm=True, stem=True, join=True)
    words = [w for w in words if ('/Noun' in w or '/Verb' in w or '/Adjective' in w)] ## XR 없음
    return words

def okt_tokenize(sent):
    words = sent.split()
    words = [w for w in words if ('/Noun' in w or '/Verb' in w or '/Adjective' in w)] ## XR 없음
    return words

def kkma_tokenizer(sent):
    kkma = Kkma()
    words = kkma.pos(sent, join=True)
    words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
    return words

def kkma_tokenize(sent):
    words = sent.split()
    words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)] 
    return words

def summarize(text, konlpy):
    reviews = []
    for r in text:
        reviews.append(re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", r))
        
    review_sents = []
    for r in reviews:
        for i in split_sentences(r):
            review_sents.append(i)
    
    if konlpy == 'komoran':
        summarizer = KeysentenceSummarizer(
            tokenize = komoran_tokenizer,
            min_sim = 0.3,
            verbose = False
        )
        keysents = summarizer.summarize(review_sents, topk=5)
        for _, _, sent in keysents:
            print(sent)
        komoran = Komoran()
        review_komoran = []
        for r in reviews:
            word_pos = ''
            for word, pos in komoran.pos(r):
                word_pos += word+'/'+pos+' '
            review_komoran.append(word_pos)
        keyword_extractor = KeywordSummarizer(
            tokenize = komoran_tokenize,
            window = -1,
            verbose = False
        )
        keywords = keyword_extractor.summarize(review_komoran, topk=10)
        keyword = ''
        for word, rank in keywords:
            if '/NN' in word:
                keyword += (word.split('/')[0]+' ')
            else:
                continue
        print(f'KEYWORD : {keyword}')
        
    elif konlpy == 'okt':
        summarizer = KeysentenceSummarizer(
            tokenize = okt_tokenizer,
            min_sim=0.3,
            verbose=False
        )
        keysents = summarizer.summarize(review_sents, topk=5)
        for _, _, sent in keysents:
            print(sent)
        okt = Okt()
        review_okt = []
        for r in reviews:
            word_pos = ''
            for word, pos in okt.pos(r):
                word_pos += word+'/'+pos+' '
            review_okt.append(word_pos)
        keyword_extractor = KeywordSummarizer(
            tokenize = okt_tokenize,
            window = -1,
            verbose = False
        )
        keywords = keyword_extractor.summarize(review_okt, topk=10)
        keyword = ''
        for word, rank in keywords:
            if '/Noun' in word:
                keyword += (word.split('/')[0]+' ')
            else:
                continue
        print(f'KEYWORD : {keyword}')
    
    elif konlpy == 'kkma':
        summarizer = KeysentenceSummarizer(
            tokenize = kkma_tokenizer,
            min_sim=0.3,
            verbose=False
        )
        keysents = summarizer.summarize(review_sents, topk=5)
        for _, _, sent in keysents:
            print(sent)
        kkma = Kkma()
        review_kkma = []
        for r in reviews:
            word_pos = ''
            for word, pos in kkma.pos(r):
                word_pos += word+'/'+pos+' '
            review_kkma.append(word_pos)
        keyword_extractor = KeywordSummarizer(
            tokenize = kkma_tokenize,
            window = -1,
            verbose = False
        )
        keywords = keyword_extractor.summarize(review_kkma, topk=10)
        keyword = ''
        for word, rank in keywords:
            if '/NN' in word:
                keyword += (word.split('/')[0]+' ')
            else:
                continue
        print(f'KEYWORD : {keyword}')


# +
def komoran_sw_tokenizer(sent):
    words = komoran.pos(sent, join=True)
    sw_words = []
    for w in words:
        if w.split('/')[0] not in stopwords:
            sw_words.append(w)
    words = [w for w in sw_words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
    return words

def komoran_sw_tokenize(sent):
    words = sent.split()
    sw_words = []
    for w in words:
        if w.split('/')[0] not in stopwords:
            sw_words.append(w)
    words = [w for w in sw_words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
    return words

def okt_sw_tokenizer(sent):
    words = okt.pos(sent, norm=True, stem=True, join=True)
    sw_words = []
    for w in words:
        if w.split('/')[0] not in stopwords:
            sw_words.append(w)
    words = [w for w in sw_words if ('/Noun' in w or '/Verb' in w or '/Adjective' in w)] ## XR 없음
    return words

def okt_sw_tokenize(sent):
    words = sent.split()
    sw_words = []
    for w in words:
        if w.split('/')[0] not in stopwords:
            sw_words.append(w)
    words = [w for w in sw_words if ('/Noun' in w or '/Verb' in w or '/Adjective' in w)] ## XR 없음
    return words

def kkma_sw_tokenizer(sent):
    kkma = Kkma()
    words = kkma.pos(sent, join=True)
    sw_words = []
    for w in words:
        if w.split('/')[0] not in stopwords:
            sw_words.append(w)
    words = [w for w in sw_words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)] 
    return words

def kkma_sw_tokenize(sent):
    words = sent.split()
    sw_words = []
    for w in words:
        if w.split('/')[0] not in stopwords:
            sw_words.append(w)
    words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)] 
    return words

def summarize_withoutsw(text, konlpy):
    reviews = []
    for r in text:
        reviews.append(re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", r))
        
    review_sents = []
    for r in reviews:
        for i in split_sentences(r):
            review_sents.append(i)
    
    if konlpy == 'komoran':
        summarizer = KeysentenceSummarizer(
            tokenize = komoran_sw_tokenizer,
            min_sim = 0.3,
            verbose = False
        )
        keysents = summarizer.summarize(review_sents, topk=5)
        for _, _, sent in keysents:
            print(sent)
        komoran = Komoran()
        review_komoran = []
        for r in reviews:
            word_pos = ''
            for word, pos in komoran.pos(r):
                word_pos += word+'/'+pos+' '
            review_komoran.append(word_pos)
        keyword_extractor = KeywordSummarizer(
            tokenize = komoran_sw_tokenize,
            window = -1,
            verbose = False
        )
        keywords = keyword_extractor.summarize(review_komoran, topk=10)
        keyword = ''
        for word, rank in keywords:
            if '/Noun' in word:
                keyword += (word.split('/')[0]+' ')
            else:
                continue
        print(f'KEYWORD : {keyword}')
        
    elif konlpy == 'okt':
        summarizer = KeysentenceSummarizer(
            tokenize = okt_sw_tokenizer,
            min_sim=0.3,
            verbose=False
        )
        keysents = summarizer.summarize(review_sents, topk=5)
        for _, _, sent in keysents:
            print(sent)
        okt = Okt()
        review_okt = []
        for r in reviews:
            word_pos = ''
            for word, pos in okt.pos(r):
                word_pos += word+'/'+pos+' '
            review_okt.append(word_pos)
        keyword_extractor = KeywordSummarizer(
            tokenize = okt_sw_tokenize,
            window = -1,
            verbose = False
        )
        keywords = keyword_extractor.summarize(review_okt, topk=10)
        keyword = ''
        for word, rank in keywords:
            if '/Noun' in word:
                keyword += (word.split('/')[0]+' ')
            else:
                continue
        print(f'KEYWORD : {keyword}')
    
    elif konlpy == 'kkma':
        summarizer = KeysentenceSummarizer(
            tokenize = kkma_sw_tokenizer,
            min_sim=0.3,
            verbose=False
        )
        keysents = summarizer.summarize(review_sents, topk=5)
        for _, _, sent in keysents:
            print(sent)
        kkma = Kkma()
        review_kkma = []
        for r in reviews:
            word_pos = ''
            for word, pos in kkma.pos(r):
                word_pos += word+'/'+pos+' '
            review_kkma.append(word_pos)
        keyword_extractor = KeywordSummarizer(
            tokenize = kkma_sw_tokenize,
            window = -1,
            verbose = False
        )
        keywords = keyword_extractor.summarize(review_kkma, topk=10)
        keyword = ''
        for word, rank in keywords:
            if '/NN' in word:
                keyword += (word.split('/')[0]+' ')
            else:
                continue
        print(f'KEYWORD : {keyword}')


# -

def summarize_wb(text, konlpy, biasword=['영화', 5]):
    reviews = []
    for r in text:
        reviews.append(re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", r))
        
    review_sents = []
    for r in reviews:
        for i in split_sentences(r):
            review_sents.append(i)

    bias = np.ones(len(review_sents))
    for i,s in enumerate(review_sents):
        if biasword[0] in s:
            bias[i] = biasword[1]
    
    if konlpy == 'komoran':
        summarizer = KeysentenceSummarizer(
            tokenize = komoran_tokenizer,
            min_sim = 0.3,
            verbose = False
        )
        keysents = summarizer.summarize(review_sents, topk=5, bias=bias)
        for _, _, sent in keysents:
            print(sent)
        komoran = Komoran()
        review_komoran = []
        for r in reviews:
            word_pos = ''
            for word, pos in komoran.pos(r):
                word_pos += word+'/'+pos+' '
            review_komoran.append(word_pos)
        keyword_extractor = KeywordSummarizer(
            tokenize = komoran_tokenize,
            window = -1,
            verbose = False
        )
        keywords = keyword_extractor.summarize(review_komoran, topk=10)
        keyword = ''
        for word, rank in keywords:
            if '/NN' in word:
                keyword += (word.split('/')[0]+' ')
            else:
                continue
        print(f'KEYWORD : {keyword}')
        
    elif konlpy == 'okt':
        summarizer = KeysentenceSummarizer(
            tokenize = okt_tokenizer,
            min_sim=0.3,
            verbose=False
        )
        keysents = summarizer.summarize(review_sents, topk=5, bias=bias)
        for _, _, sent in keysents:
            print(sent)
        okt = Okt()
        review_okt = []
        for r in reviews:
            word_pos = ''
            for word, pos in okt.pos(r):
                word_pos += word+'/'+pos+' '
            review_okt.append(word_pos)
        keyword_extractor = KeywordSummarizer(
            tokenize = okt_tokenize,
            window = -1,
            verbose = False
        )
        keywords = keyword_extractor.summarize(review_okt, topk=10)
        keyword = ''
        for word, rank in keywords:
            if '/Noun' in word:
                keyword += (word.split('/')[0]+' ')
            else:
                continue
        print(f'KEYWORD : {keyword}')
    
    elif konlpy == 'kkma':
        summarizer = KeysentenceSummarizer(
            tokenize = kkma_tokenizer,
            min_sim=0.3,
            verbose=False
        )
        keysents = summarizer.summarize(review_sents, topk=5, bias=bias)
        for _, _, sent in keysents:
            print(sent)
        kkma = Kkma()
        review_kkma = []
        for r in reviews:
            word_pos = ''
            for word, pos in kkma.pos(r):
                word_pos += word+'/'+pos+' '
            review_kkma.append(word_pos)
        keyword_extractor = KeywordSummarizer(
            tokenize = kkma_tokenize,
            window = -1,
            verbose = False
        )
        keywords = keyword_extractor.summarize(review_kkma, topk=10)
        keyword = ''
        for word, rank in keywords:
            if '/NN' in word:
                keyword += (word.split('/')[0]+' ')
            else:
                continue
        print(f'KEYWORD : {keyword}')


# #### 시사회 리뷰+다른 거 있는 블로그1

with open('시사회.txt', encoding='utf-8') as f:
    review = [sent.strip() for sent in f]

review

summarize(review, 'komoran')

summarize_withoutsw(review, 'komoran')

summarize_wb(review, 'komoran', ['시사회',5])

summarize(review, 'okt')

summarize_wb(review, 'okt')

summarize_wb(review, 'okt', ['시사회', 5])

## norm = True, stem = True
summarize(review, 'okt')

summarize_withoutsw(review, 'okt')

## norm = True, stem = True
summarize_withoutsw(review, 'okt')

summarize(review, 'kkma')

summarize_wb(review, 'kkma')

summarize_wb(review, 'kkma', ['시사회',5])

summarize_withoutsw(review, 'kkma')

# #### 시사회 리뷰+다른 거 있는 블로그2

with open('blog_text.txt', encoding='utf-8') as f:
    review = [sent.strip() for sent in f]

summarize(review, 'komoran')

summarize_wb(review, 'komoran')

summarize_wb(review, 'komoran', ['시사회',5])

summarize_withoutsw(review, 'komoran')

summarize(review, 'okt')

## norm = True, stem = True
summarize(review, 'okt')

summarize_withoutsw(review, 'okt')

## norm = True, stem = True
summarize_withoutsw(review, 'okt')

summarize(review, 'kkma')

summarize_wb(review, 'kkma', ['시사회', 5])

summarize_withoutsw(review, 'kkma')

# #### 시사회 리뷰만 있는

with open('blog_text2.txt', encoding='utf-8') as f:
    review = [sent.strip() for sent in f]

summarize(review, 'komoran')

summarize_withoutsw(review, 'komoran')

summarize_wb(review, 'komoran')

summarize_wb(review, 'komoran', ['시사회',5])

summarize(review, 'okt')

## norm = True, stem = True
summarize(review, 'okt')

summarize_wb(review, 'okt', ['시사회',5])

summarize_withoutsw(review, 'okt')

## norm = True, stem = True
summarize_withoutsw(review, 'okt')

summarize(review, 'kkma')

summarize_wb(review, 'kkma')

summarize_wb(review, 'kkma', ['시사회',5])

summarize_withoutsw(review, 'kkma')

# #### 시사회 리뷰만 있는2

with open('blog_text3.txt', encoding='utf-8') as f:
    review = [sent.strip() for sent in f]

summarize(review, 'komoran')

summarize_withoutsw(review, 'komoran')

summarize(review, 'okt')

## norm = True, stem = True
summarize(review, 'okt')

summarize_withoutsw(review, 'okt')

## norm = True, stem = True
summarize_withoutsw(review, 'okt')

summarize(review, 'kkma')

summarize_withoutsw(review, 'kkma')

# #### 시사회 리뷰만 있는3

with open('blog_text5.txt', encoding='utf-8') as f:
    review = [sent.strip() for sent in f]

summarize(review, 'komoran')

summarize_withoutsw(review, 'komoran')

summarize(review, 'okt')

## norm = True, stem = True
summarize(review, 'okt')

summarize_withoutsw(review, 'okt')

## norm = True, stem = True
summarize_withoutsw(review, 'okt')

summarize(review, 'kkma')

summarize_withoutsw(review, 'kkma')

# #### 시사회 리뷰만 있는4

with open('blog_text4.txt', encoding='utf-8') as f:
    review = [sent.strip() for sent in f]

summarize(review, 'komoran')

summarize_withoutsw(review, 'komoran')

summarize(review, 'okt')

## norm = True, stem = True
summarize(review, 'okt')

summarize_withoutsw(review, 'okt')

## norm = True, stem = True
summarize_withoutsw(review, 'okt')

summarize(review, 'kkma')

summarize_withoutsw(review, 'kkma')

# ### 10점 리뷰

sentence = '''시도한 만큼의 실패 - 박쥐======================= 많은 장르변용의 시도들 가운데서도 선례가 드물만큼 다양한 장르를 하나로 융합하려 한 박쥐는 불행하게도 그만큼이나 다양한 종류의 헛점만을 두드러지게 노출시킨 영화가 되고 말았다. 가장 실망스러운 점은 역시 차용한 장르의 수가 과하다는 데에 기인한다. 각각의 장르적 특성들은 적절한 타협점을 찾지 못한 채 때로는 상충하며 때로는 스스로 의미를 잃은 채 표류한다. 특히 종교와 인간성에 관한 심도있는 주제의식은 러닝타임 내내 블랙코미디적 요소나 스플래터 호러형식과 반발을 일으키면서 영화 전체의 내용적 표층을 엷게 만든다. 한층 더 유감스러운 것은, 이런 문제점의 부각이 차용의 대상이 되는 장르의 수가 지나치게 많다는 것에만 원인을 두고 있는 것이 아니라는 점이다. 장르의 융합이나 변형 등 장르변용의 성공 사례들은 하나같이 대상이 될 장르 본연의 속성을 재현하는 데에 영화의 상당부분을 할애하기 마련인데(이것은 장르규칙의 준수, 특정작품과 유사한 스타일의 구사, 오마주나 클리셰의 삽입 등 매우 다양한 수단들을 통해 구현된다) 박쥐는 이 점에서 너무도 안일한 대처를 보여준다. 장르 룰은 무시되기 일쑤고, 장르형식은 시간의 흐름에 따라 필요할 때 잠시(그리고 가벼이) 사용되고는 이내 버려진다. 이 영화는 상당 부분 치정극 형식에 의지하고 있으므로 김옥빈을 사이에 둔 두 남자의 대립구조와 여기에서 파생하는 긴장감의 형성은 장르특성상 불가결한 것이었음에도 불구하고 영화 내에서의 신하균의 역할 비중은 이해하기 힘들 정도로 적다(신하균이 분한 강우라는 인물은 죽음 직전의 순간까지도 주인공 남녀의 관계를 알아채지 못한다, 게다가 마지막 깨달음의 한순간 던지는 대사의 무의미함은 듣는이를 망측하게 할 정도이다) 김옥빈이 맡은 팜므파탈로서의 역할 또한 부족한 점이 많은데 이는 배우 개인의 능력보다는 캐릭터 자체의 설정상, 표현상의 무성의(또는 무절제)함이 가져온 결과로 보인다. 오히려 김옥빈의 연기는 인물색채의 근본적인 옅음을 일정수준 보완해 낼만큼 긍정적인 효과를 가져오는 것이었다(이것은 기대하지 않았기에 더더욱 반가운 점이다.) 덕분에 태주라는 인물이 가지는 냉혹함과 아이같은 잔인함은 어느 정도 표현될 수가 있었다. 하지만 그와 동시에 애처로움이 느껴질 정도로 어눌하기 짝이없는 여자로 묘사된 점(영화에서 태주의 악랄한 음모가 폭로되는 것은 믿기 어렵게도 태주 본인의 입을 통해서였다)은 아무래도 납득하기가 힘들다. 아울러 주연 여배우의 작품에 대한 기여도(라고 적고 노출도 라고 읽음 :>)에 비해 여주인공의 뇌쇄적인 매력은 제대로 드러나지 못한 점이나 악녀라고 하기엔 터무니 없을정도로 부실한 계획성으로 일관하고 있는 점 등으로 볼 때 이 영화의 팜므파탈 구현 의도는 다분히 실패에 가깝다고 할 수밖에 없다. 한편 어쩌면 이 작품의 일차적인 목표이었을지도 모를 시종일관 두드러지게 나타나는 특징이 있는데 그것은 특정한 몇몇 대사와 장면들에 대한 애착이 노골적으로 드러난다는 점이다. 여기에 해당되는 대사라 함은 거의가(나의 기억으로는 '전부'이긴 하지만...) 블랙코미디에 근거한 유머들인데 사실 이런 조크들이 그 자체로서 나쁘다는 것은 아니다. 오히려 몇몇 대사들은 썩 좋은 편에 속한다. 문제는 그런 괜찮은 농담들을 이끌어내는 과정이 매우 억지스럽다는 데에 있다. 감독의 전작들이 서사의 큰 줄기를 거스르지 않은 채 능숙한 솜씨로 원하는 상황을 온전히 이끌어낸 후에야 이 작품과 유사한(물론 빈도는 훨씬 낮지만) 이른바 블랙 코미디를 시도하는 데에 비해 박쥐는 오히려 미리 준비된 몇 가지의 농담들을 위해 시나리오 전체가 끼워 맞추어진 듯한 인상마저 풍긴다. 다분히 의도적인 듯한 '쎈' 장면들의 잦은 배열도 마찬가지로 한 편의 영화로서의 일관성보다도 우선하여 고려된 듯한 느낌을 주는데, 여기서 짚고 넘어가야 할 것은 그런 장면들이 이전에 만들어진 다른 작품들의 특정 장면을 연상시키게 하는 경우가 많다는 점이다. 체내의 피가 역류하는 장면의 송강호의 얼굴 클로즈업은 렛미인의 인상적인 한 장면을 연상하게 하며, 인간의 능력을 훌쩍 뛰어넘는 존재들(이면서 또한 연인관계인) 간의 무지막지하고 약간은 우스꽝스럽기도 한 격투장면에서는 핸콕의 한 장면이 떠오른다. 박쥐에서 가장 인상적이라고 할 수 있는 후반부의 희한한 흡혈장면(이마저도 이전의 잦은 흡혈 장면들 덕분에 온전히 힘을 발휘하고 있지 못하지만)또한 상이한 개체간의 기묘한 융합을 즐겨 다루는 미이케 다케시와 친숙한 관객이라면 오히려 식상함을 느낄 터이다. 어쨋거나 놀라운 것은 이런 매끄럽지 못한 만듦새를 보아서도 이 감독에 대한 오랜 동안의 신뢰와 경외를 저버리기는 너무도 힘이 든다는 점이다. 아무래도 형식과 내용 전반에 걸친 부족함을 감수해내면서까지 시도해 보고자하는 흥미로운 실험거리가 있었던 건 아닐까 조심스레 추측해 본다. 만일 그런 것이라면 감독의 모든 '갈증'은 이 한편의 영화로써 완전히 해소되었기만을 바랄 뿐이다. '''

sentences = split_sentences(sentence)

sentences

summarize(sentences, 'komoran')

summarize_withoutsw(sentences, 'komoran')

summarize(sentences, 'okt')

summarize_withoutsw(sentences, 'okt')

summarize(sentences, 'kkma')

summarize_withoutsw(sentences, 'kkma')
