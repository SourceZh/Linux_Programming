#!/usr/local/bin/python3
import sys

###################################
# 	A simple word frequency count 
# program. Nothing to say.
#					DoubleZ
#					2015.05.10
###################################


def usage():
	print("Usage - "+sys.argv[0]+" N")
	print("		Where N is in [1,5]")
	exit(0)

def ngram(text, n):
	words_freq={}
	textlength = len(text)
	for i in range(textlength-(n-1)):
		word = text[i:i+n]
		if word not in words_freq:
			words_freq[word] = 1
		else:
			words_freq[word] = words_freq[word]+1
	return words_freq


if __name__ == '__main__':
	argv = sys.argv
	argvLength = len(argv)
	if (argvLength != 2):
		usage()

	N = argv[1]
	Num = int(N)
	if Num not in range(1,6):
		usage()

	text = ""
	try:
		file = open('Corpus', 'r')
	except FileNotFoundError:
		print("Error: file not found! Please make sure Corpus file has been download!")
	else:
		for line in file:
			text += line.rstrip('\n')
		file.close()

	words_freq = ngram(text, Num)

	filename = N+"Gram"
	file = open(filename, 'w')
	for word in sorted(words_freq, key=words_freq.get, reverse=True):
		file.write(word+":"+str(words_freq[word])+"\n")

	file.close()
	print("The result is store at "+filename)
