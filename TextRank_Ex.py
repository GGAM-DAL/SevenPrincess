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

from Module import *

with open('시사회.txt', encoding='utf-8') as f:
    review = [sent.strip() for sent in f]

sr1 = TextRank(review).summarize()
sr1
