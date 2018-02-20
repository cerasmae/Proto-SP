import sys, os, re, unittest
import unicodedata
from itertools import islice

# MAIN

# tokenizes the words, leaves out names
def tokenizer(all_lines):
	count = 1
	prev_string = ""
	for line in all_lines:

		curr_line = line.split()
		# print curr_line, len(curr_line), curr_line[len(curr_line)-1]

		if count == 2: # gets the year of the date

			file_name = "corpus/"+curr_line[len(curr_line)-1]+"-corpus.txt"
			print file_name

			if os.path.exists(file_name):
				type_action = "a"
			else:
				type_action = "w"

			corpus = open(file_name, type_action)

		elif count > 3: # start to tokenize at line 4 of the current file

			written = False
			title = 0
			proper_noun = False
			if curr_line:
				for i in range( len(curr_line) ):
					curr_string = curr_line[i]
					written = False
					proper_noun = False
					
					if curr_string.istitle():
						title = 1
						if prev_string is not "":
							last_ch = prev_string[len(prev_string)-1]
							if last_ch != "." and last_ch != ")":
								proper_noun = True

						if not proper_noun:
							cleaned_str = re.sub(r'[^A-Za-z.\\\'-]', '', curr_string)
							cleaned_str = cleaned_str.lower()
							
							if cleaned_str[len(cleaned_str)-1] == ".":
								cleaned_str = cleaned_str[:-1]

							corpus.write(cleaned_str +"\n")
							written = True

					else:
						title = 2
						cleaned_str = re.sub(r'[^A-Za-z.\\\'-]', '', curr_string)
						cleaned_str = cleaned_str.lower()

						if len(cleaned_str) >- 0:
							if cleaned_str[len(cleaned_str)-1] == ".":
								cleaned_str = cleaned_str[:-1]

							corpus.write(cleaned_str +"\n")
							written = True

					print curr_string, written, title
					prev_string = curr_string

		count += 1

	corpus.close()


def main():
	path = "/home/cerasmae/Desktop/SP/cleaned-data";
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
			

			try:
				curr_file = open(file_path)
				lines = curr_file.read().splitlines()
				curr_file.close()
				# tokenizer(lines)

				# testing purposes
				if count == 1:
					# print count, file_path
					tokenizer(lines)
					# for line in lines:
					# 	print line
				else:
					True
					# print count, file_path

				

				# code to print out specific number of lines only
				# with open(file_path) as curr_file:
				# 	# head = [next(curr_file) for x in xrange(2)]
				# 	head = list(islice(curr_file, 2))

				# 	print head
				# 	count = count + 1
				# 	True

			except IOError:
				print ("could not read") 

			count += 1

	except IOError:
		print ("something is probably wrong with the path")

main()
