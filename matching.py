# https://dev.to/coderasha/compare-documents-similarity-using-python-nlp-4odp
import string

import nltk
import gensim
import numpy as np
nltk.download('punkt')
from nltk.tokenize import word_tokenize , sent_tokenize
from bs4 import BeautifulSoup
import requests
import pandas as pd

#split sentence into words
# data = "Mars is approximately half the diameter of Earth."
# print(word_tokenize(data))
#
# #split paragraph into sentences
# para = "Mars is a cold desert world. It is half the size of Earth. "
# print(sent_tokenize(para))

def get_weights(filename = 'relavo.txt', txt_or_lst = "txt"): # txt is inputing a txt file, str is inputing a list[string] file.
    file_docs = []
    if txt_or_lst == 'txt':
        with open (str(filename)) as f:
            tokens = sent_tokenize(f.read())
            for line in tokens:
                file_docs.append(line)
    else:
        file_docs = filename
    # print("Number of documents:",len(file_docs))

    #Tokenize words and create dictionary

    gen_docs = [[w.lower() for w in word_tokenize(text)]
                for text in file_docs]
    # print(gen_docs)
    dictionary = gensim.corpora.Dictionary(gen_docs)
    # print(dictionary.token2id)

    # create a bag of words
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    # print(corpus)

    # TFIDF Term Frequency – Inverse Document Frequency(TF-IDF)
    # words that occur more frequently across the documents get bigger weights.
    tf_idf = gensim.models.TfidfModel(corpus)
    lst = []
    for doc in tf_idf[corpus]:
        lst.append([[dictionary[id], np.around(freq, decimals=2)] for id, freq in doc])
        # print([[dictionary[id], np.around(freq, decimals=2)] for id, freq in doc])


    #  This section is to remove all the words that are not relavent : integers, punctuation, for, from, to, the, etc.
    prep = ("when","or","further","is","claim","wherein","that","keep","causes","a","and","are","be","an","aboard","about","above","across","after","against","along","amid","among","anti","around","as","at","before","behind","below","beneath","beside","besides","between","beyond","but","by","concerning","considering"
    ,"despite","down","during","except","excepting","excluding","following","for","from","in","inside","into","like","minus","near","of","off","on","onto","opposite","outside","over","past","per","plus","regarding","round","save","since"
    ,"than","through","to","toward","towards","under","underneath","unlike","until","up","upon","versus","via","with","within","without")
    dic = {}
    for item in lst:
        for i in item:
            if i[0] not in dic.keys():
                dic[i[0]] = i[1]
            else:
                dic[i[0]] = round(dic[i[0]] + i[1], 2)

    dic_copy = dic.copy()
    for key, val in dic_copy.items():
        if key in string.punctuation or key in prep:
            dic.pop(key)
        try:
          (int(key))
          dic.pop(key)
        except:
          continue

    return dic
if __name__ == '__main__':
    # relavo = get_weights('relavo.txt')
    results = {}
    file = pd.ExcelFile('Relavo_patent_search_keywords.xlsx')
    print("Loading file successful, the sheets names are: ", file.sheet_names) # to view the sheets name
    df = file.parse("All_search_results")
    res = df['result link']
    len = 1 #res.__len__()

    for i in range(len):
        URL = res[i]
        # desktop user-agent
        # ###################################
        #IMPORTANT                              go to chrome, search my user agent, copy the User agent into the User_agent down below.
        # ###################################
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"

        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")

    # df.insert(location, 'result link', val)  # how to insert into the pd frame
    # results.to_excel('relavo patent with Relevance weight', index=False) # how to export the data