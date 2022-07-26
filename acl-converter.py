#!/usr/bin/python
# -*- coding: utf-8 -*-

from fw_rule import *


def processLines(lines, src_f, dst_f, args):

    src_f = eval(src_f)(args)
    dst_f = eval(dst_f)(args)

    print dst_f.header()

    r_lines = [ replace_token(l, src_f.to_replace).split() for l in lines if not str_contains(l, src_f.invalid) ]
    #print r_lines
    
    for d in [ src_f.to_rule(r) for e in [ expand_list(l) for l in [ replace_exp_ip(rl) for rl in r_lines if len(rl) ] ] for r in e ]:
        # print d
        print dst_f.from_rule(d)
        # print
    
    print dst_f.footer()


def convertFile(params):
    in_file, src_f, dst_f, args = params
    
    if in_file != '_stdin_':
        try:	
            with open(in_file) as i_file:
                lines = i_file.readlines()
        except IOError:      
            print 'File %s not available!' % in_file
            sys.exit()
    else:
        lines = sys.stdin
    
    processLines(lines, src_f, dst_f, args)


def checkArgs(args):
    rtr = []
    basename = args[0].split('/')[-1]
    
    if '2' in basename:
        in_f, out_f = basename.split('2')[:2]
        if len(in_f) and len(out_f):
            rtr = ['_stdin_', in_f, out_f, []]

            drt = 'in'
            intf_d = {}          
            e_args = args[1:]
            i = 0

            while len(e_args):
                if i == 0:
                    if e_args[0] != '-':
                        rtr[0] = e_args[0]
                
                if i == 1:
                    for intfs in [ i_lst.split('=') for i_lst in e_args[0].split(',') ]:
                        if len(intfs) > 1:
                            intf_d[intfs[0]] = intfs[1]
               
                if i == 2:
                    if e_args[0] in ['in', 'out', 'both']:
                        drt = e_args[0]
  
                e_args = e_args[1:]
                i += 1
            
            rtr[3] = [drt, intf_d]

    return rtr


if __name__ == "__main__":
    params = checkArgs(sys.argv)

    # print params
    if len(params):
        convertFile(params)
    
# End of acl-converter.py


