#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import string, re

def removeHexCharacters():
    f = open('errors.txt', 'r')

    urls = f.read().splitlines()
    f.close()

    checkpoint = urls

    count = 0

    for url in urls:

    	with open(url, 'r') as curr_file:
    		content = curr_file.read()

    	curr_file.close()

	try:
		True
		content = content.decode('utf').encode('ascii', errors='ignore')

	except Exception, e:
		err_file = open('errors_of_errors.txt', 'a')
		err_file.write(url + "\n")
		err_file.close()


    	# print content

    	with open(url, 'w') as curr_file:
    		curr_file.write(content)

    	curr_file.close()

    	count = count + 1

    	checkpoint.remove(url)

    	with open('errors.txt', 'w') as err_file:
    		for cp in checkpoint:
    			err_file.write(cp + "\n")
    	err_file.close()


    	print url


removeHexCharacters()

    