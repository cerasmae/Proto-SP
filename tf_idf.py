from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import sys, os, re, unittest
import unicodedata
import json

def init(path):
	ac_data = []
	with open(path, mode = "r") as ac:
		ac_data = json.load(ac)
	ac.close()
	return ac_data

# print ac_data[0]

def tfidf_unigram(corpus):
	tfidf_vectorizer = TfidfVectorizer(min_df = 1)
	TF_X = tfidf_vectorizer.fit_transform(corpus)
	idf = tfidf_vectorizer.idf_

	result_dict = dict(zip(tfidf_vectorizer.get_feature_names(), idf))

	result_file = open("tfidfresults/tf_idf_ac_results.json", "w")
	json.dump(result_dict, result_file)
	result_file.close()

def tfidf_unigram_root(corpus):
	tfidf_vectorizer = TfidfVectorizer(min_df = 1)
	TF_X = tfidf_vectorizer.fit_transform(corpus)
	idf = tfidf_vectorizer.idf_

	result_dict = dict(zip(tfidf_vectorizer.get_feature_names(), idf))

	result_file = open("tfidfresults/tf_idf_ac_results.json", "w")
	json.dump(result_dict, result_file)
	result_file.close()

def tfidf_wordbigram(corpus):
	tfidf_vectorizer = TfidfVectorizer(ngram_range=(2, 2), min_df = 1)
	TF_X = tfidf_vectorizer.fit_transform(corpus)
	idf = tfidf_vectorizer.idf_

	result_dict = dict(zip(tfidf_vectorizer.get_feature_names(), idf))

	result_file = open("tfidfresults/tf_idf_wb_results.json", "w")
	json.dump(result_dict, result_file)
	result_file.close()

def tfidf_charbigram(corpus):
	tfidf_vectorizer = TfidfVectorizer(ngram_range=(2, 2), token_pattern="[A-Za-z]", min_df = 1, analyzer="char", )
	TF_X = tfidf_vectorizer.fit_transform(corpus)
	idf = tfidf_vectorizer.idf_

	result_dict = dict(zip(tfidf_vectorizer.get_feature_names(), idf))

	result_file = open("tfidfresults/tf_idf_cb_results.json", "w")
	json.dump(result_dict, result_file)
	result_file.close()

def main():
	all_corpus = "corpus/all-corpus.json"
	ac_data = init(all_corpus)

	tfidf_wordbigram(ac_data)
	tfidf_charbigram(ac_data)


main()