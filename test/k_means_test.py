import sys
import os
from app.core.tf_idf import buildIndex, tfidfWeighting
from app.core.k_means import cosineSimilarity, distance
from app.core.k_means import centroidInit, k_means, silhouette

from test import is_almost_equal


def test_cosine_similarity():
    term_dict = {
        ('d1', 'langit'): 1,
        ('d1', 'hari'): 1,
        ('d1', 'ini'): 1,
        ('d1', 'biru'): 1,
        ('d1', 'matahari'): 0,
        ('d1', 'cerah'): 0,
        ('d1', 'di'): 0,
        ('d2', 'langit'): 0,
        ('d2', 'hari'): 1,
        ('d2', 'ini'): 1,
        ('d2', 'biru'): 0,
        ('d2', 'matahari'): 1,
        ('d2', 'cerah'): 1,
        ('d2', 'di'): 0,
        ('d3', 'langit'): 1,
        ('d3', 'hari'): 0,
        ('d3', 'ini'): 0,
        ('d3', 'biru'): 0,
        ('d3', 'matahari'): 1,
        ('d3', 'cerah'): 1,
        ('d3', 'di'): 1
    }

    another_term_dict = {
        ('d4', 'langit'): 0,
        ('d4', 'hari'): 0,
        ('d4', 'ini'): 0,
        ('d4', 'biru'): 0,
        ('d4', 'matahari'): 2,
        ('d4', 'cerah'): 1,
        ('d4', 'di'): 0,
        ('d5', 'langit'): 1,
        ('d5', 'hari'): 1,
        ('d5', 'ini'): 0,
        ('d5', 'biru'): 0,
        ('d5', 'matahari'): 0,
        ('d5', 'cerah'): 0,
        ('d5', 'di'): 1
    }

    tf_idf = tfidfWeighting(buildIndex(term_dict))
    another_tf_idf = tfidfWeighting(buildIndex(another_term_dict))
    d1 = tf_idf['d1']
    d2 = tf_idf['d2']
    d3 = tf_idf['d3']
    d4 = another_tf_idf['d4']
    d5 = another_tf_idf['d5']

    assert is_almost_equal(cosineSimilarity(d1, d1), 1, 5)
    assert is_almost_equal(cosineSimilarity(d2, d2), 1, 5)
    assert is_almost_equal(cosineSimilarity(d3, d3), 1, 5)
    assert is_almost_equal(cosineSimilarity(d4, d4), 1, 5)

    assert is_almost_equal(cosineSimilarity(d1, d4), 0, 5)
    assert is_almost_equal(cosineSimilarity(d1, d3), 0.0966982251958593, 5)
    assert is_almost_equal(cosineSimilarity(d2, d4), 0.701132322497753, 5)
    assert is_almost_equal(cosineSimilarity(d2, d3), 0.310963382403555, 5)
    assert is_almost_equal(cosineSimilarity(d3, d4), 0.436052957032722, 5)
    assert is_almost_equal(cosineSimilarity(d1, d2), 0.310963382403555, 5)


def test_centroid_init():
    term_dict = {
        ('d1', 'langit'): 1,
        ('d1', 'hari'): 1,
        ('d1', 'ini'): 1,
        ('d1', 'biru'): 1,
        ('d1', 'matahari'): 0,
        ('d1', 'cerah'): 0,
        ('d1', 'di'): 0,
        ('d2', 'langit'): 0,
        ('d2', 'hari'): 1,
        ('d2', 'ini'): 1,
        ('d2', 'biru'): 0,
        ('d2', 'matahari'): 1,
        ('d2', 'cerah'): 1,
        ('d2', 'di'): 0,
        ('d3', 'langit'): 1,
        ('d3', 'hari'): 0,
        ('d3', 'ini'): 0,
        ('d3', 'biru'): 0,
        ('d3', 'matahari'): 1,
        ('d3', 'cerah'): 1,
        ('d3', 'di'): 1
    }

    tf_idf = tfidfWeighting(buildIndex(term_dict))

    centroid = centroidInit(2, tf_idf)
    assert len(centroid) == 2
    assert centroid[0].index.isin([
        'langit', 'hari', 'ini', 'biru', 'matahari', 'cerah', 'di'
    ]).all()
    assert centroid[1].index.isin([
        'langit', 'hari', 'ini', 'biru', 'matahari', 'cerah', 'di'
    ]).all()


def test_silhouette():
    term_dict = {
        ('d1', 'langit'): 1,
        ('d1', 'hari'): 1,
        ('d1', 'ini'): 1,
        ('d1', 'biru'): 1,
        ('d1', 'matahari'): 0,
        ('d1', 'cerah'): 0,
        ('d1', 'di'): 0,
        ('d2', 'langit'): 0,
        ('d2', 'hari'): 1,
        ('d2', 'ini'): 1,
        ('d2', 'biru'): 0,
        ('d2', 'matahari'): 1,
        ('d2', 'cerah'): 1,
        ('d2', 'di'): 0,
        ('d3', 'langit'): 1,
        ('d3', 'hari'): 0,
        ('d3', 'ini'): 0,
        ('d3', 'biru'): 0,
        ('d3', 'matahari'): 1,
        ('d3', 'cerah'): 1,
        ('d3', 'di'): 1
    }

    tf_idf = tfidfWeighting(buildIndex(term_dict))
    cluster_result = [['d1', 'd2'], ['d3']]
    silhouette_data = silhouette(tf_idf, cluster_result)
    print(silhouette_data)
    print(len(tf_idf))
    d1 = list(filter(lambda x: x[0] == 'd1', silhouette_data[0]))[0][1]
    d2 = list(filter(lambda x: x[0] == 'd2', silhouette_data[0]))[0][1]
    d3 = list(filter(lambda x: x[0] == 'd3', silhouette_data[1]))[0][1]
    assert is_almost_equal(d1, 0.237202187778446, 5)
    assert is_almost_equal(d2, 0, 5)
    assert is_almost_equal(d3, 0, 5)
    assert is_almost_equal(silhouette_data['avg'], 0.0790673959261488, 5)
