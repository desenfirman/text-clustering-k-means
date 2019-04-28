import re
import os
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pandas as pd
import numpy as np
import copy
import itertools
import random as rd


def getFileListing(dir_name):
    file_list = []
    for file in os.listdir(dir_name):
        file_name = os.fsdecode(file)
        path_file = dir_name + "/" + file_name
        file_list.append(path_file)
    return file_list


def openFile(article_file_name):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    with open(article_file_name, "r") as article_file:
        article = article_file.read()
        article = re.sub('[^A-Za-z\s]+', ' ', article).casefold()
        article = stemmer.stem(article)
        return article


def addArticle(term_dict, article_file_name):
    article = openFile(article_file_name)
    article = article.split()
    doc_index = "d" + str(
        os.path.splitext(os.path.basename(article_file_name))[0])
    for word in article:
        if (doc_index, word) in term_dict:
            term_dict[(doc_index, word)] += 1
        else:
            term_dict[(doc_index, word)] = 1
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
    for term, row in tf_index.iterrows():
        for doc_index in row.keys():
            if (index[doc_index][term] != 0):
                N = len(row)
                non_zero_el = [row[i] for i in row.keys() if row[i] > 0]
                wtf = 1 + np.log10(index[doc_index][term])
                df = len(non_zero_el)
                idf = np.log10(N / df)
                tf_index[doc_index][term] = (wtf * idf)

    # normalize vector space
    for doc_index in tf_index:
        d_resultant = 0
        for term in tf_index[doc_index].keys():
            d_resultant += np.square(tf_index[doc_index][term])
        d_resultant = np.sqrt(d_resultant)
        sums = 0
        for term in tf_index[doc_index].keys():
            tf_index[doc_index][term] = tf_index[doc_index][term] / d_resultant
            sums += tf_index[doc_index][term]
        # print(sums)
    return tf_index


def cosineSimilarity(doc_1, doc_2):
    sums = 0
    for row in doc_1.keys():
        sums += doc_1[row] * doc_2[row]
    return sums


def centroidInitImproved(k, index_weighted):
    doc_list = [x for x in index_weighted]
    doc_couple = list(itertools.combinations(doc_list, 2))

    distance_sum = 0
    for doc_1, doc_2 in doc_couple:
        distance_sum += cosineSimilarity(
            index_weighted[doc_1], index_weighted[doc_2])

    mean_dist = distance_sum / len(doc_couple)
    return mean_dist


def distance(doc_1, doc_2):
    return 1 - cosineSimilarity(doc_1, doc_2)


def euc_distance(doc_1, doc_2):
    sums = 0
    for row in doc_1.keys():
        sums += np.square((doc_1[row] - doc_2[row]))
    return np.sqrt(sums)


def centroidInit(k, index_weighted):
    selected_doc = [index_weighted[('d' + str(
        rd.randint(1, len(index_weighted.columns))))] for i in range(k)]
    return selected_doc


def updateCentroid(index_weighted, centroid, cluster_member):
    centroid = copy.deepcopy(centroid)
    new_cluster_member = copy.deepcopy(cluster_member)
    for c_id in range(len(centroid)):
        centroid[c_id] = (
            index_weighted[new_cluster_member[c_id]].mean(axis=1))
    # print(new_centroid)
    return centroid


def k_means(k, index_weighted, iterasi):
    centroid = centroidInit(k, index_weighted)

    t = 0
    while(t < iterasi):
        cluster_member = [[] for c in range(len(centroid))]
        doc_min_data = list()
        for doc_index in index_weighted:
            dst = list()
            for c in range(len(centroid)):
                d = distance(centroid[c], index_weighted[doc_index])
                # print(d)
                # print(centroid)
                dst.append(d)
            c_selected = dst.index(min(dst))
            # print(c_selected)
            cluster_member[c_selected].append(doc_index)
            doc_min_data.append(min(dst))
        print(np.mean(doc_min_data))
        # print(cluster_member)
        # update centro
        # print(n_centroid)
        # print(centroid)

        c_temp = updateCentroid(index_weighted, centroid, cluster_member)
        centroid = []
        centroid = c_temp

        t += 1
    return cluster_member


def silhouette(index_weighted, cluster_result):
    for doc_index in index_weighted:
        c = [ix for ix, row in enumerate(
            cluster_result) for iy, i in enumerate(row) if i == doc_index]

        a = 0
        for x in cluster_result[c[0]]:
            a += distance(index_weighted[x], index_weighted[doc_index])
        a = a / len(cluster_result[c[0]])
        other_cluster = list()
        for x, val in enumerate(cluster_result):
            if x != c[0]:
                b_temp = 0
                for y in val:
                    b_temp += distance(
                        index_weighted[y], index_weighted[doc_index])
                b_temp = b_temp / len(val)
                other_cluster.append(b_temp)
        b = min(other_cluster)
        sil = (b - a) / max([a, b])

        print("Silhoueete ", doc_index, " :", sil)

        # for x in cluster_result:


def addDirectory(file_listing):
    term_dict = dict()
    for file_path in file_listing:
        term_dict = addArticle(term_dict, file_path)
    return term_dict


file_list = getFileListing("./artikel")

term_dict = dict()
term_dict = addDirectory(file_list)
index = buildIndex(term_dict)
index_weighted = tfidfWeighting(index)
print(cosineSimilarity(index_weighted['d9'], index_weighted['d14']))
