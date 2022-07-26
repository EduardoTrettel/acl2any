#!/usr/bin/python 

import sys
import time
from acl_functions import *


def ipfw_convert(acl, ilist, tid):
        log = 0
        dct = 'any' # Traffic direction: 'in', 'out' or 'both'
        src_port = 'null'
        dst_port = 'null'
        intf = 'null'
        r_params = []

	r1 = acl.replace('{ ','').replace(' }', '').replace(' or ', '|')
	r1 = r1.replace('dst-port ', '').replace('src-port ', '').replace('setup', '')
        r1 = r1.replace('allow', 'pass').replace('deny', 'block').replace('count','match')
	r2 = r1.split()
        l2 = len(r2)
        #print r1.replace('\n', '')

        idx = 1 # First element (index 0) is ipfw rule number
        
        # Rule action is the next token  
        action = r2[idx]
        idx += 1

        # Next token is either 'log' or the protocol name
        if r2[idx] == 'log':
            log = 1
            idx += 1
        proto = r2[idx]
        idx += 2 # Skip 'from' statement

        # Next one is the source (IP or list)
        src_ip = r2[idx]
        idx += 1
        
        # If the next token is not 'to', then a source port is being specified here.
        # Otherwise we skip to the next one, supposed to be the destination (IP or list).
        if r2[idx] != 'to':
            src_port = r2[idx]
            idx += 2
        else:
            idx += 1

        dst_ip = r2[idx]
        idx+=1

        # By now we can have already reached the end of the list, so we check the index against the
        # array length.
        if l2 > idx:
            # A destination port is specified?
            if not r2[idx].isalpha():
                dst_port = r2[idx]
                if l2 > idx+1: 
                    idx+=1
            # Direction of traffic. If not found, defaults to 'any'
            if ( r2[idx] == 'in' ) or ( r2[idx] == 'out' ):
                dct = r2[idx]
                if l2 > idx+1: idx+=1
            # Traffic applies to a specific interface? Otherwise, it applies to all of them.
            if r2[idx] == 'via':
                intf = r2[idx+1]

        # Generates XML for every acl
        for si in gen_ip_list(src_ip):
            for sp in gen_port_list(src_port):
                for di in gen_ip_list(dst_ip):
                    for dp in gen_port_list(dst_port):
                        r_params = [ action, intf, log, dct, proto, si, sp, di, dp, tid ]
                        prtxml(r_params, ilist)
           


if __name__ == "__main__":
    nargs = len(sys.argv) - 1
    ilist = {}

    # First argument is the file with the 'ipfw show' output.
    if nargs > 0:
	in_file = sys.argv[1]

        # Next argument are supposed to be interface aliases.
        if nargs > 1:
            ilist = { a.split('=')[0]: a.split('=')[1] for a in sys.argv[2:]}

	epoch = int(time.strftime('%s'))

        try:
	    with open(in_file) as acl_file:
	        xmltag(0,'filter','','s')
		for acl in acl_file.readlines():
                    if ( '!' not in acl ) and ( 'established' not in acl ) and ( 'frag' not in acl ):
		        ipfw_convert(acl, ilist, str(epoch))
                        epoch+=1
	        xmltag(0,'filter','','e')
        except IOError:
            print 'File %s not available!' % in_file
    else:
        print 'Usage: ipfw2pfsense.py ipfw-acl-file [interface-match-list]'
        print '       [interface-match-list] = [ em0=wan em1=lan ... ]'

#
# End of ipfw2pfsense.py
#
