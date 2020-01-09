import os
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import copy
import pandas as pd
import numpy as np


factory = StemmerFactory()
stemmer = factory.create_stemmer()


def getFileListing(dir_name):
    file_list = []
    for file in os.listdir(dir_name):
        file_name = os.fsdecode(file)
        path_file = dir_name + "/" + file_name
        file_list.append(path_file)
    return file_list


def openFile(article_file_name):
    with open(article_file_name, "r") as article_file:
        article = article_file.read()
        article = re.sub('[^A-Za-z\s]+', ' ', article).casefold()
        article = stemmer.stem(article)
        return article


def getTitle(article_file_name):
    with open(article_file_name, "r") as article_file:
        return article_file.readline()


def addArticle(term_dict, article_file_name):
    article = openFile(article_file_name)
    article = article.split()
    doc_index = str(
        os.path.splitext(os.path.basename(article_file_name))[0])
    for word in article:
        if (doc_index, word) in term_dict:
            term_dict[(doc_index, word)] += 1
        else:
            term_dict[(doc_index, word)] = 1
    return term_dict


def tokenize(file_listing):
    term_dict = dict()
    for file_path in file_listing:
        term_dict = addArticle(term_dict, file_path)
    return term_dict


def buildIndex(term_dict):
    cols = set([doc_index for (doc_index, term) in term_dict.keys()])
    rows = set([term for (doc_index, term) in term_dict.keys()])
    index = pd.DataFrame(index=rows, columns=cols)
    index = index.fillna(0.0)

    for key, value in term_dict.items():
        index[key[0]][key[1]] = value
    return index


def tfidfWeighting(index):
    tf_index = copy.deepcopy(index)
    for term, row in index.iterrows():
        for doc_index in row.keys():
            if (index[doc_index][term] != 0):
                N = len(row)
                non_zero_el = [row[i] for i in row.keys() if row[i] > 0]
                wtf = 1 + np.log10(index[doc_index][term])
                df = len(non_zero_el)
                idf = np.log10(N / df)
                tf_index[doc_index][term] = (wtf * idf)
    return tf_index
