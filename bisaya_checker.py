import json
try:
	from urllib.request import urlopen
	from urllib import parse as urlparse
except ImportError:
	from urllib2 import urlopen, urlparse

from bs4 import BeautifulSoup

def check_words():

	rw_data = {}

	with open("removed_words.json", "r") as rw:
		rw_data = json.load(rw)

	rw.close()
	count = 1
	for rw_datum in rw_data:
		try:
			url1 = "http://www.binisaya.com/node/21?search=binisaya&word="
			url2 = "&Search=Search"
			final = url1 + rw_datum + url2
			# example = "http://www.binisaya.com/node/21?search=binisaya&word=example&Search=Search"
			page = urlopen(final)
			soup = BeautifulSoup(page, 'html.parser')

			# result = soup.find('form', {'name': 'form1'})
			# child_result = result.findChildren()
			# print result

			# texts = soup.findAll(text = True)
			# visible_texts = filter(tag_visible, texts)
			# print u" ".join(t.strip() for t in visible_texts)
			# print texts

			[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]

			visible_text = soup.getText()
			results = " ".join(visible_text.split())
			res = ""
			if "No results found" in results:
				rw_data[rw_datum] = 1
				res = "not found, english word"
			else:
				rw_data[rw_datum] = 0
				res = "found, bisaya word"

			print count, rw_datum, res

			count = count + 1
		except Exception, e:
			print repr(e)

	with open("removed_words.json", "w") as rw:
		json.dump(rw_data, rw)

	rw.close()

check_words()


