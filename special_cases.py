#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys, os, re, unittest
import unicodedata
import json
from itertools import islice
# https://www.loc.gov/standards/iso639-2/php/code_list.php
from langdetect import detect

# MAIN 

# tokenizes the words, leaves out names

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def notALink(str):
	link = False

	if ".com" not in str and ".org" not in str:
		link = True
	if "http" not in str:
		link = link and True

	return link

def tokenizer(all_lines):
	print "inside tokenizer"
	count = 1
	corpus_data = {}
	prev_string = ""
	valid_data = []
	new = True
	curr_data = {}
	curr_date = ""
	for line in all_lines:
		line = line.decode('latin1').encode('latin1').decode('utf8')
		curr_line = line.split()
		# print curr_line, len(curr_line), curr_line[len(curr_line)-1]

		if count == 1:
			# print line
			curr_data['title'] = line.upper()

		elif count == 2: # gets the year of the date

			if "-" in curr_line[0]:
				# print "splitting by - here"
				curr_line = curr_line[0].split("-")

			curr_date = curr_line[len(curr_line)-1]

			file_name = "sc/"+curr_date+"-corpus.json"

			if os.path.exists(file_name):
				type_action = "r"
				new = False
			else:
				type_action = "w"
				new = True

			# print file_name, new, type_action

			
			
			if not new:
				# print "not new: " + file_name
				corpus = open(file_name)
				corpus_data = json.load(corpus)
				# print corpus_data
				# print "why"
			else:
				corpus = open(file_name, "w")
				corpus_data = {}
				corpus_data['corpus'] = []
				# json.dump(corpus_data-, corpus)
			corpus.close()

			curr_data['date'] = line

		elif count == 3:
			curr_data['author'] = line.upper()

		elif count > 3: # start to tokenize at line 4 of the current file

			written = False
			title = 0
			proper_noun = False
			if curr_line:
				for i in range( len(curr_line) ):
					curr_string = curr_line[i]
					written = False
					proper_noun = False
					
					if curr_string.istitle(): # if the first letter of the word is uppercase
						title = 1
						if prev_string is not "": 	# if the word is not the very first word of the document
							last_ch = prev_string[len(prev_string)-1]
							if last_ch != "." and last_ch != ")" and last_ch != "!" and last_ch != "?" and last_ch != ":" and last_ch != "\"": 	# checks if the previous string has a period .
								proper_noun = True					# it's a proper noun if there is no . in the prev_str

						if not proper_noun:

							if not hasNumbers(curr_string) and notALink(curr_string):	# check if string does not have any number or any ".com" to signify a link
								cleaned_str = re.sub(r'[^A-Za-zÀ-ÿ.\\\'-]', '', curr_string.decode('latin1').encode('latin1').decode('utf8'))	# removes other characters that are not alphabet and selected symbols
								cleaned_str = cleaned_str.lower()
								
								if cleaned_str[len(cleaned_str)-1] == ".":
									cleaned_str = cleaned_str[:-1]

								# if cleaned_str not in valid_data:	# checks if current cleaned string is unique
								valid_data.append(cleaned_str)

								# corpus.write(cleaned_str +"\n")
								written = True

							else:
								written = False

					else:
						title = 2
						
						if not hasNumbers(curr_string) and notALink(curr_string): # check if string does not have any number or any ".com" to signify a link
							cleaned_str = re.sub(r'[^A-Za-z.\\\'-]', '', curr_string)
							cleaned_str = cleaned_str.lower()

							if len(cleaned_str) > 0:
								if cleaned_str[len(cleaned_str)-1] == ".":
									cleaned_str = cleaned_str[:-1]

								# json.dump(cleaned_str, corpus, ensure_ascii=False)
								# corpus.write(cleaned_str +"\n")
								
								# if cleaned_str not in valid_data: # checks if current cleaned string is unique
								valid_data.append(cleaned_str)

								written = True

						else:
							written = False

					# if written:
					# 	print curr_string, written, title, detect(curr_string.decode('utf-8').strip())
					# else:
					# 	print curr_string, written, title


					prev_string = curr_string

		count += 1

	valid_data = check_english_dict(valid_data)

	# print valid_data, "what"
	valid_string = ""
	for datum in valid_data:
		valid_string = valid_string + datum + " "

	valid_string = valid_string.strip()

	curr_data['words'] = valid_string

	corpus_data['corpus'].append(curr_data)
	corpus = open(file_name, "w")
	json.dump(corpus_data, corpus)
	# or
	# for vd in valid_data:
	# 	corpus.write(vd+"\n")

	corpus.close()

	unique_dict = dict((el, 1) for el in valid_data)

	# code for th-e unique corpus
	if os.stat(UNIQUE_CORPUS).st_size > 2:
		# print "not empty"
		with open(UNIQUE_CORPUS, mode = "r") as uc:
			uc_data = json.load(uc)
		uc.close()

		with open(UNIQUE_CORPUS, mode = "w") as uc:
			for curr_str in valid_data:
				uc_data[curr_str] = 1
			json.dump(uc_data, uc)
		uc.close()
	else:
		with open(UNIQUE_CORPUS, mode = "w") as uc:
			json.dump(unique_dict, uc)
		uc.close()

	# code for word corpus
	wc_file_name = "sc_wcorpus/"+curr_date+"-corpus.txt"
	wcorpus_data = {}

	if os.path.exists(wc_file_name):
		new = False
	else:
		new = True


	if not new:
		wcorpus = open(wc_file_name)
		wcorpus_data = json.load(wcorpus)
		wcorpus.close()

	wcorpus = open(wc_file_name, "w")
		# json.dump(corpus_data-, corpus)
	for v_datum in valid_data:
		wcorpus_data[v_datum] = 1
		# wcorpus_data.append(v_datum)

	json.dump(wcorpus_data, wcorpus)
	wcorpus.close()

	all_corpus = "sc/all-corpus.json"
	ac_data = []
	# code for all corpus
	if os.stat(all_corpus).st_size > 0:
		# print "not empty"
		with open(all_corpus, mode = "r") as ac:
			ac_data = json.load(ac)
		ac.close()

		with open(all_corpus, mode = "w") as ac:
			ac_data.append(valid_string)
			json.dump(ac_data, ac)
		ac.close()
	else:
		with open(all_corpus, mode = "w") as ac:
			ac_data.append(valid_string)
			json.dump(ac_data, ac)
		ac.close()


def unique_corpus(valid_data):
	corpus_file = open("corpus/2009-corpus.txt", "w")
	corpus_data = json.load(corpus_file)

	print "in unique_corpus", valid_data

	for curr_str in valid_data:
		if curr_str not in corpus_data:
			corpus_data.append(currstr)

	json.dump(corpus_data, corpus_file)

	corpus_file.close()


def check_english_dict(valid_data):
	eng_dict = open("words_dictionary.json", "r")
	eng_dict_data = json.load(eng_dict)
	eng_dict.close()

	words = valid_data
	removed_words = []

	for i in range(len(words)):
		try:
			if eng_dict_data[words[i]] == 1:
				# words.remove(words[i])
				removed_words.append(words[i])

		except Exception, e:
			print "check english dict 1st exception"
			repr(e)

	# print removed_words

	try:
		wordsjson = open("removed_words.json", "r")
		rw_data = json.load(wordsjson)
		wordsjson.close()


		wordsjson = open("removed_words.json", "w")

		for removed_word in removed_words:
			rw_data[removed_word] = 1

		json.dump(rw_data, wordsjson)
		wordsjson.close()

	except Exception, e:
		print "check english dict 2nd exception"
		print repr(e)

	return words


def remove_words():
	wordsjson = open("removed_words.json", "r")
	rw_data = json.load(wordsjson)
	wordsjson.close()

	to_remove = []

	for words in rw_data:
		if rw_data[words] == 0:
			to_remove.append(words)

	print to_remove

	for tr_word in to_remove:
		rw_data.pop(tr_word)

	print "after"
	print rw_data

	wordsjson = open("removed_words.json", "w")
	json.dump(rw_data, wordsjson)
	wordsjson.close()

	eng_dict = open("words_dictionary.json", "r")
	eng_dict_data = json.load(eng_dict)
	eng_dict.close()

	for tr_word in to_remove:
		try:
			eng_dict_data.pop(tr_word)

		except Exception, e:
			print "removed words exception"
			repr(e)

	eng_dict = open("words_dictionary.json", "w")
	json.dump(eng_dict_data, eng_dict)
	eng_dict.close()

def trying():
	corpus_file = open("words_dictionary.json", "r")
	corpus_data = json.load(corpus_file)
	val = 0

	print "in trying"

	try:
		val = corpus_data["bahog"]
	except Exception, e:
		print repr(e)
		val = -1

	# print corpus_data

	# for curr_str in valid_data:
	# 	if curr_str not in corpus_data:-
	# 		corpus_data.append(currstr)

	# json.dump(corpus_data, corpus_file)

	corpus_file.close()
	print val



def main():
	# path = "/home/cerasmae/Desktop/Celine-Thesis/cleaned-data";
	# https://stackoverflow.com/questions/30265592/list-directories-python-osx
	

	# bomboradyo-scrape
	# path = "/Users/rl-14/Desktop/Celine-Thesis/all-data/bomboradyo-scrape/error"
	# bismag data
	# path = "/Users/rl-14/Desktop/Celine-Thesis/all-data/cleaned-data"
	# all data
	path = "/Users/rl-14/Desktop/Celine-Thesis/all-data-reordered/all"
	# special cases
	path = "/Users/rl-14/Desktop/Celine-Thesis/all-data-reordered/special_cases"

	sys.path.append(path)
	# files = os.listdir(path)
	try:

		files = [x for x in os.listdir(path) if x.endswith(".txt")]
		count = 1
		# for file in files:
		# 	file_path = path+"/"+file

		# 	F = open(file_path, "r")

		# 	print(count, F)
		# 	count += 1

		for file in files:
			file_path = path+"/"+file
			# print file

			try:
				curr_file = open(file_path)
				lines = curr_file.read().splitlines()
				curr_file.close()
				# tokenizer(lines)

				# testing purposes

				# print count, file

				# if count <= 15:
				print count, file
				tokenizer(lines)
					# check_duplicate()
					# for line in lines:
					# 	print line
				# else:
				# 	print count, "here"
					# break
					# print count, file_path

			except Exception, e:
				err_file = open('sc_errors.txt', 'a')
				err_file.write(file_path + "\n")
				err_file.close()
				print "2nd last exception"
				print repr(e)

			count += 1

	except Exception, e:
		print "last exception"
		print repr(e)

	print "done"

# UNIQUE_CORPUS = "/home/cerasmae/Desktop/SP/Proto-SP/corpus/unique-corpus.json"
UNIQUE_CORPUS = "/Users/rl-14/Desktop/Celine-Thesis/Proto-SP/corpus/unique-corpus.json"
# with open(UNIQUE_CORPUS, mode = "w") as uc:
# 	json.dump([], uc)
# uc.close()


main()
# remove_words()
# trying()


# code to print out specific number of lines only
				# with open(file_path) as curr_file:
				# 	# head = [next(curr_file) for x in xrange(2)]
				# 	head = list(islice(curr_file, 2))

				# 	print head
				# 	count = count + 1
				# 	True