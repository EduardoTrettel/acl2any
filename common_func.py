#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
from itertools import product

# Print n Tabs
ntabs = lambda n: ''.join(['\t'] * n)

# Returns a tuple from a range like '139-445', e.g.
prt_tuple = lambda s: tuple((s + '-' + s).split('-')[:2])

# Adds a '/32' after a ip address that is not in CIDR format
add_32 = lambda s: s + '/32' if '.' in s and '/' not in s else s

# Remove a '/32' from a CIDR address
del_32 = lambda s: s.replace('/32','')

# Returns a list with both the IP addr and mask from a CIDR
from_cidr = lambda s: s.split('/') if '.' and '/' in s else ['','']

# Returns a XML tag with given value. Multi-line tags can be
# created with (s)tart or (e)nd marks.
def xmltag(n, tag, value='', ml=''):
    sep = '/'
    if len(ml):
        if ml == 's':
            sep = ''
        r_str = '<%s%s>' % (sep, tag)
    else:
        r_str = '<%s>%s</%s>\n' % (tag, value, tag)

    return ntabs(n) + r_str

# Convert ip into a DNS lookup or network description 
def lookup(ip):
    addr, mask = from_cidr(ip)
    if mask == '32':
        try:
            lr = socket.gethostbyaddr(addr)
            rtr = lr[0] 
            if len(lr[1]):
                rtr += ' ' + ' '.join(lr[1]) 
            rtr += ' (' + addr + ')'
        except socket.herror:
            rtr = ip
    elif mask != '':
        rtr = 'Rede %s' % ip
    else:
        rtr = ip

    return rtr


# Check if any of the substrings in str_set is 
# present in input string i_str
def str_contains(i_str, str_set):
    cnd = False

    for s in str_set:
        if s in i_str:
            cnd = True
            break

    return cnd


# Process a string rule, replacing the necessary tokens
def replace_token(line, to_replace):
    l = line

    for t in to_replace:      
        l = l.replace(t[0],t[1])
    
    return l


# Returns a IP list from a string like CDIR_1[|CIDR_2[:IP1,IP2,..,IPn]]
def gen_ip_lst(i_str):
    last_oct = []
    ip, ip_l = i_str.split(':')
    ip = '.'.join(ip.split('.')[:-1]) + '.'

    for octet in ip_l.split(','):
        if '-' in octet:
            x, y = [ int(i) for i in octet.split('-') ]
            last_oct.extend(range(x,y+1))
        else:
            last_oct.append(int(octet))

    r_str = ','.join([ ip + str(o) for o in last_oct ])

    return r_str


# Returns a list of IPs addresses after expanding them using gen_ip_lst (above) 
def replace_exp_ip(lst, exp_sep = ['|', ':']):
    # print lst
    r_lst = [ ','.join([ gen_ip_lst(s) if ':' in s else s for s in l.split('|') ]) if str_contains(l, exp_sep) else l for l in lst ]

    return r_lst

# "Clones" lst for every IP present that conforms to the pattern 
def expand_list(lst):
    r_lst = []
    
    t_lst = [ [i, lst[i].split(',')] for i in range(len(lst)) if ',' in lst[i] ]
    
    if len(t_lst):
        i_lst = [ t[0] for t in t_lst]

        for e in [ list(x) for x in product(*[t[1] for t in t_lst]) ]:
            nl = lst[:]
            for i in range(len(e)):
                nl[i_lst[i]] = e[i]
            r_lst.append(nl)
    else:
        r_lst = [lst]

    return r_lst    
            


# Dummy main function
#
if __name__ == "__main__":
    pass

#
# End of common_func.py
#

