import enum
from os import remove
from nltk import stem
from nltk import tokenize
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re, ast
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

#load data using pandas
def fxprocessing(file):
    data = pd.DataFrame(file)

    #remove duplicate
    #remove_duplicate = pd.DataFrame(data).drop_duplicates()

    #remove username & link
    #data['remove_user'] = np.vectorize(remove_pattern(tweet= data['tweet'],pattern=r"@[\w]*"))
    #data['remove_link'] = np.vectorize(remove_pattern(tweet=data['remove_user'], pattern=r"https?:\/\/.*[\r\n]*"))
    data['remove_user'] = np.vectorize(remove_pattern)(tweet= data['tweet'],pattern=r"@[\w]*")
    data['remove_link'] = np.vectorize(remove_pattern)(tweet=data['remove_user'], pattern=r"https?:\/\/.*[\r\n]*")
    data['casefolding'] = np.vectorize(casefolding)(tweet=data['remove_link'])
    data['token'] = np.vectorize(token)(tweet=data['casefolding'])
    data['remove_slang'] = np.vectorize(remove_slang)(token=data['token'])
    data['stemming'] = np.vectorize(remove_sw)(slang_removed=data['remove_slang'])

    return data['casefolding']

def remove_pattern(tweet, pattern):
    r = re.findall(pattern, tweet)
    for i in r:
        tweet = re.sub(i, '', tweet)
        tweet = re.sub(i, '', tweet)
    return tweet

#casefolding
def casefolding(tweet):
    tweet = tweet.lower()
    tweet = re.sub(r'[^\w\s]','', tweet)
    tweet = re.sub(r'#','',tweet)
    return tweet

#tokenize
def token(tweet):
    tokenizer = TweetTokenizer(preserve_case= False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)
    #print(tweet_tokens)
    return ",".join(tweet_tokens)

def remove_slang(token):
    #jadiin array lagi
    #make .split(",") 
    file = open("slang_words.txt","r")
    contents = file.read()

    kata_baku = ast.literal_eval(contents)
    keys = kata_baku.keys()
    file.close()

    kata = token.split(",")
    #kata = token
    for idx, word in enumerate(kata):
        if word in keys:
            kata[idx] = kata_baku.get(word)                                                                                                                                                  
    return ",".join(kata) #udah text


def remove_sw(slang_removed):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    sentence = slang_removed.replace(","," ")
    output = stemmer.stem(sentence)

    return output.replace(" ",", ")
    #listStopword = set(stopwords.words('indonesian'))
    #remove_stopwords = [word for word in slgrmvd if word not in listStopword]

    #hasil_stemming = []
    # for kata in remove_stopwords:
    #     hasil_stemming.append(stemmer.stem(kata))
    # return hasil_stemming