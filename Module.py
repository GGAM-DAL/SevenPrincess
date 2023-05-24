from textrank import KeysentenceSummarizer
from textrank import KeywordSummarizer
import re
from kss import split_sentences
from konlpy.tag import Komoran, Kkma

f = open('stopwords-ko.txt','r', encoding='utf-8')
stopwords = f.read().splitlines()

def komoran_tokenizer(sent):
    komoran = Komoran()
    words = komoran.pos(sent, join=True)
    words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
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

class TextRank:
    def __init__(self, text):
        self.text = text

    def summarize(self):
        reviews = ''
        for r in self.text:
            reviews += (re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", r) + ' ')

        review_sents = []
        for i in split_sentences(reviews):
            review_sents.append(i)

        if len(reviews) < 2000:
            summarizer = KeysentenceSummarizer(
                tokenize=komoran_tokenizer,
                min_sim=0.3,
                verbose=False
            )
            keysents = summarizer.summarize(review_sents, topk=3)
            sents = ''
            for _, _, sent in keysents:
                sents += (sent+' ')

        elif len(reviews) >= 2000:
            summarizer = KeysentenceSummarizer(
                tokenize=kkma_sw_tokenizer,
                min_sim=0.3,
                verbose=False
            )
            keysents = summarizer.summarize(review_sents, topk=3)
            sents = ''
            for _, _, sent in keysents:
                sents += (sent+' ')
        return sents