import sys, os, re, unittest
from itertools import islice

# MAIN

def main():
	path = "/home/cerasmae/Desktop/SP/data";
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

				if count == 1:
					print count, file_path
					for line in lines:
						print line
				else:
					print count, file_path

				count += 1

				

				# code to print out specific number of lines only
				# with open(file_path) as curr_file:
				# 	# head = [next(curr_file) for x in xrange(2)]
				# 	head = list(islice(curr_file, 2))

				# 	print head
				# 	count = count + 1
				# 	True

			except IOError:
				print ("could not read", file_path) 

	except IOError:
		print ("something is probably wrong with the path")

main()
