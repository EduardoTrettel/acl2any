#!/usr/bin/python

import sys
import time

def xmltag(ntab, tag, text, style='sl'):
	tabs = ''
	for i in range(ntab): tabs = tabs + '\t'
	s_tag = '<%s>' % tag
	e_tag = '</%s>' % tag
	if style == 's':
		out = s_tag
	elif style == 'e':
		out = e_tag
	else:
		out = s_tag + text + e_tag 
	
	print tabs + out


def acl2list(acl):
	rule = acl.replace('host ', '').replace('permit', 'pass').replace('deny', 'block').replace('\n', '').split()
	r1 = normalize(3,rule)
	r2 = normalize(5,r1)
	if '.' in r2[-1] or r2[-1] == 'any':
		r2.append('null')
	
	return r2

def normalize(n, lst):
	if n < len(lst):
		if lst[n] == 'range':
			port = lst[n+1] + '-' + lst[n+2]
			del lst[n:n+2]
			lst[n] = port
		elif lst[n] == 'eq':
			del lst[n]
		elif lst[n] == 'gt':
			port = str(int(lst[n+1])+1) + '-65535'
			del lst[n]
			lst[n] = port
		else:
			lst.insert(n, 'null')

	return lst


def prtxml(acl):
	xmltag(1,'rule','','s')
	rule = acl2list(acl)
	xmltag(2,'tracker',time.strftime('%s'))
	xmltag(2,'type',rule[0])
	xmltag(2,'interface','wan')
	xmltag(2,'ipproto','inet')
	xmltag(2,'direction','in')
	if rule[1] != 'ip':
		xmltag(2,'protocol',rule[1])
	xmltag(2,'source','','s')
	src = rule[2]
	if src == 'any':
		xmltag(3,'any','')
	else:
		xmltag(3,'address',src)
	port = rule[3]
	if port != 'null': xmltag(3,'port',port)
	xmltag(2,'source','','e')
	xmltag(2,'destination','','s')
	dst = rule[4]
	if dst == 'any':
		xmltag(3,'any','')
	else:
		xmltag(3,'address',dst)
	port = rule[5]
	if port != 'null': xmltag(3,'port',port)
	xmltag(2,'destination','','e')
	if rule[-1] == 'log': xmltag(2,'log','')
	xmltag(1,'rule','','e')
	time.sleep(1)

if __name__ == "__main__":
	in_file = sys.argv[1]

	xmltag(0,'filter','','s')

	with open(in_file) as acl_file:
		for acl in acl_file.readlines():
			if '!' not in acl and 'access' not in acl:
				prtxml(acl)
	
	xmltag(0,'filter','','e')


