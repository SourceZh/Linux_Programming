#!/usr/local/bin/python3

filename = '红楼梦.txt'
dict = {}
symble = {' ', '\n', '，', '“', '”', '：', '《', '》', '"', '．', '？', '！', '*', '-', '_', '(', ')', '。', '　', "'", '`', ',', '.', '—', ':', '‘', '、', '’', '?', '<', '>', '!', ';', '', ']', '['}
file = open(filename, 'r')
for line in file:
	for i in range(len(line)):
		word = line[i]
		if word not in symble:
			if word not in dict:
				dict[word] = 1
			else:
				dict[word] = dict[word]+1
file.close();
file = open('output', 'w')
for key in sorted(dict, key=dict.get, reverse=True):
	file.write(key+':'+str(dict[key])+'\t')
file.close();