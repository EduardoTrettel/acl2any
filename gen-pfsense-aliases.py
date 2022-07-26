#!/usr/bin/python

import sys
import time
from acl_functions import *


def gen_aliases(acl):
    ip_lst = ""
    xmltag(1,'alias','','s')
    r1 = acl.replace('{ ','').replace(' }', '').replace('"', '').replace('=',',').replace('\n','').replace(' or ', '|')
    r2 = r1.split(',')
    xmltag(2,'name',r2[0])
    if '.' in r2[1]:
        xmltag(2,'type','network')
    else:
        xmltag(2,'type','port')
    xmltag(2,'address',' '.join(gen_ip_list(r2[1])))
    xmltag(1,'alias','','e')


if __name__ == "__main__":
    nargs = len(sys.argv) - 1

    if nargs > 0:
	in_file = sys.argv[1]

        try:
	    with open(in_file) as acl_file:
	            xmltag(0,'aliases','','s')
		    for acl in acl_file.readlines():
                        if ( '#' not in acl ):
		            gen_aliases(acl)
	            xmltag(0,'aliases','','e')
        except IOError:
            print 'File %s not available!' % in_file
    else:
        print 'Usage: gen-pfsense-aliases.py alias_file'

#
# End of gen-pfsense-aliases.py
#
