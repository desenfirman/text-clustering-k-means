import sys
import os
from app.core.tf_idf import addArticle, tokenize, getFileListing
from app.core.tf_idf import buildIndex, tfidfWeighting
from test import is_almost_equal


def test_add_article():
    term_dict = {}
    term_dict = addArticle(term_dict, "test/sample_corpus/1.txt")
    expected_term_dict = {
        ('1', "ini"): 1,
        ('1', "budi"): 2,
        ('1', "main"): 1,
        ('1', "bola"): 1,
        ('1', "di"): 1,
        ('1', "lapang"): 1,
        ('1', "sama"): 1,
        ('1', "teman"): 2
    }
    file_2 = "test/" + \
             "sample_corpus/kesalahan_bikin_dovizioso.txt"
    term_dict_2 = addArticle(term_dict, file_2)

    expected_term_dict = {
        ('1', "ini"): 1,
        ('1', "budi"): 2,
        ('1', "main"): 1,
        ('1', "bola"): 1,
        ('1', "di"): 1,
        ('1', "lapang"): 1,
        ('1', "sama"): 1,
        ('1', "teman"): 2,
        ('kesalahan_bikin_dovizioso', "salah"): 2,
        ('kesalahan_bikin_dovizioso', "bikin"): 1,
        ('kesalahan_bikin_dovizioso', "dovizioso"): 2,
        ('kesalahan_bikin_dovizioso', "hilang"): 2,
        ('kesalahan_bikin_dovizioso', "kans"): 2,
        ('kesalahan_bikin_dovizioso', "start"): 2,
        ('kesalahan_bikin_dovizioso', "di"): 3,
        ('kesalahan_bikin_dovizioso', "baris"): 2,
        ('kesalahan_bikin_dovizioso', "pertama"): 1,
        ('kesalahan_bikin_dovizioso', "andrea"): 1,
        ('kesalahan_bikin_dovizioso', "gembira"): 1,
        ('kesalahan_bikin_dovizioso', "bisa"): 1,
        ('kesalahan_bikin_dovizioso', "bangkit"): 1,
        ('kesalahan_bikin_dovizioso', "dari"): 1,
        ('kesalahan_bikin_dovizioso', "situasi"): 1,
        ('kesalahan_bikin_dovizioso', "buruk"): 1,
        ('kesalahan_bikin_dovizioso', "hari"): 1,
        ('kesalahan_bikin_dovizioso', "dua"): 1,
        ('kesalahan_bikin_dovizioso', "motogp"): 1,
        ('kesalahan_bikin_dovizioso', "spanyol"): 1,
        ('kesalahan_bikin_dovizioso', "namun"): 1,
        ('kesalahan_bikin_dovizioso', "buah"): 1,
        ('kesalahan_bikin_dovizioso', "akibat"): 1,
        ('kesalahan_bikin_dovizioso', "depan"): 1,
    }

    assert expected_term_dict == term_dict


def test_get_file_listing():
    dir = os.path.abspath("test/sample_corpus")
    file_list = getFileListing(dir)
    expected_file_list = [
        os.path.abspath("test/sample_corpus/1.txt"),
        os.path.abspath("test/sample_corpus/kesalahan_bikin_dovizioso.txt")
    ]
    assert file_list == expected_file_list


def test_tokenize_dir():
    dir = os.path.abspath("test/sample_corpus")
    file_list = getFileListing(dir)
    term_dict = tokenize(file_list)
    expected_term_dict = {
        ('1', "ini"): 1,
        ('1', "budi"): 2,
        ('1', "main"): 1,
        ('1', "bola"): 1,
        ('1', "di"): 1,
        ('1', "lapang"): 1,
        ('1', "sama"): 1,
        ('1', "teman"): 2,
        ('kesalahan_bikin_dovizioso', "salah"): 2,
        ('kesalahan_bikin_dovizioso', "bikin"): 1,
        ('kesalahan_bikin_dovizioso', "dovizioso"): 2,
        ('kesalahan_bikin_dovizioso', "hilang"): 2,
        ('kesalahan_bikin_dovizioso', "kans"): 2,
        ('kesalahan_bikin_dovizioso', "start"): 2,
        ('kesalahan_bikin_dovizioso', "di"): 3,
        ('kesalahan_bikin_dovizioso', "baris"): 2,
        ('kesalahan_bikin_dovizioso', "pertama"): 1,
        ('kesalahan_bikin_dovizioso', "andrea"): 1,
        ('kesalahan_bikin_dovizioso', "gembira"): 1,
        ('kesalahan_bikin_dovizioso', "bisa"): 1,
        ('kesalahan_bikin_dovizioso', "bangkit"): 1,
        ('kesalahan_bikin_dovizioso', "dari"): 1,
        ('kesalahan_bikin_dovizioso', "situasi"): 1,
        ('kesalahan_bikin_dovizioso', "buruk"): 1,
        ('kesalahan_bikin_dovizioso', "hari"): 1,
        ('kesalahan_bikin_dovizioso', "dua"): 1,
        ('kesalahan_bikin_dovizioso', "motogp"): 1,
        ('kesalahan_bikin_dovizioso', "spanyol"): 1,
        ('kesalahan_bikin_dovizioso', "namun"): 1,
        ('kesalahan_bikin_dovizioso', "buah"): 1,
        ('kesalahan_bikin_dovizioso', "akibat"): 1,
        ('kesalahan_bikin_dovizioso', "depan"): 1,
    }
    assert term_dict == expected_term_dict


def test_build_index():
    term_dict = {
        ('1', "ini"): 1,
        ('1', "budi"): 2,
        ('1', "main"): 1,
        ('1', "bola"): 1,
        ('2', "sepak"): 1,
        ('2', "bola"): 1,
        ("2", "manchester"): 1,
        ("2", "united"): 1
    }
    index = buildIndex(term_dict)
    assert index['2']['bola'] == 1.0
    assert index['2']['budi'] == 0.0
    assert index['1']['manchester'] == 0.0
    assert index['1']['united'] == 0.0


def test_tf_idf_weighting():
    term_dict = {
        ('1', "ini"): 1,
        ('1', "budi"): 2,
        ('1', "main"): 1,
        ('1', "bola"): 1,
        ('2', "sepak"): 1,
        ('2', "bola"): 1,
        ("2", "manchester"): 1,
        ("2", "united"): 1
    }
    index = buildIndex(term_dict)
    index_tf_idf = tfidfWeighting(index)
    assert index_tf_idf['2']['bola'] == 0.0
    assert index_tf_idf['1']['bola'] == 0.0
    assert index_tf_idf['2']['budi'] == 0.0
    assert index_tf_idf['1']['manchester'] == 0.0
    assert index_tf_idf['1']['united'] == 0.0
    assert is_almost_equal(index_tf_idf['1']['budi'], 0.391649053953438, 5)
    assert is_almost_equal(index_tf_idf['2']['manchester'],
                           0.301029995663981, 5)
