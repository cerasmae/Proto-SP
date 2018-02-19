import sys, os, re, unittest

# MAIN

def main():
	path = "/home/cerasmae/Desktop/SP/data";
	sys.path.append(path)
	# files = os.listdir(path)
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
			with open(file_path) as fp:
				True

		except IOError:
			print ("could not read", file_path) 

main()
