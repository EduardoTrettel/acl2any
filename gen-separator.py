#!/usr/bin/python
# -*- coding: utf-8 -*-

# from fw_rule import *
import sys
# import time
# import copy
# import socket

from common_func import *

def separator(lst, c, intf):
    rtr = ''
    colors = {'r': 'bg-danger', 'g': 'bg-success', 'b': 'bg-info', 'y': 'bg-warning'}

    pos, cl, t = lst
    nsep = 'sep' + str(c)
    nrow = 'fr' + pos
    txt = '<![CDATA[%s]]>' % t

    rtr += xmltag(3,nsep,'','s') + '\n'
    rtr += xmltag(4,'row',nrow)
    rtr += xmltag(4,'text',txt)
    rtr += xmltag(4,'color',colors[cl[0]])
    rtr += xmltag(4,'if',intf)
    rtr += xmltag(3,nsep,'','e')


    return rtr


def processLines(lines, intf):
    c = 0

    # print xmltag(1,'separator','','s')
    print xmltag(2,intf, '', 's')
    
    for lst in [ l.replace('\n','').split(',') for l in lines if '#' not in l ]:
        print separator(lst, c, intf)
        c += 1
 
    print xmltag(2,intf, '', 'e')
    # print xmltag(1,'separator','','e')


def convertFile(params):
    in_file, intf = params
    
    if in_file != '_stdin_':
        try:	
            with open(in_file) as i_file:
                lines = i_file.readlines()
        except IOError:      
            print 'File %s not available!' % in_file
            sys.exit()
    else:
        lines = sys.stdin
    
    processLines(lines, intf)


def checkArgs(args):
    rtr = ['_stdin_', 'wan']
 
    e_args = args[1:]
    i = 0

    while len(e_args):
        if i == 0:
            if e_args[0] != '-':
                rtr[0] = e_args[0]
        
        if i == 1:
            rtr[1] = e_args[0]
        
        e_args = e_args[1:]
        i += 1

    return rtr


if __name__ == "__main__":
    params = checkArgs(sys.argv)

    # print params
    if len(params):
        convertFile(params)
    
# End of acl-converter.py


