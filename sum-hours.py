#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def to_minutes(s):
    d = ':'

    if 'h' in s:
        d = 'h'    
    h, m = s.split(d)
    mins = int(h) * 60 + int(m)

    return mins


def min_to_hours(m):
    hr = '0' + str(m/60)
    mi = '0' + str(m%60)
    return '%sh%sm' % (hr[-2:], mi[-2:])


def processLines(lines):
    m_sum = 0
    ratio = 20.0

    print 'Periodo trabalhado: %s a %s\n' % (lines[0].split(' ')[0], lines[-1].split(' ')[0])
    
    for line in lines:
        d, s, e = line.split(' ')

        delta = to_minutes(e) - to_minutes(s)
        print "Horas trabalhadas dia %s: %s (%s minutos)" % (d, min_to_hours(delta), str(delta))
        m_sum += delta

    print '\nTotal de horas trabalhadas: %s (%s minutos)' % (min_to_hours(m_sum), str(m_sum))
    print 'Total devido: R$ %.2f' % (m_sum * ratio/60)
    


def convertFile(params):
    in_file = params[0]
    
    if in_file != '_stdin_':
        try:	
            with open(in_file) as i_file:
                lines = i_file.readlines()
        except IOError:      
            print 'File %s not available!' % in_file
            sys.exit()
    else:
        lines = sys.stdin
    
    processLines(lines)


def checkArgs(args):
    rtr = ['']

    if len(args) > 1:
        rtr[0] = args[1]
    else:
        rtr[0] = '_stdin_'
        
    return rtr


if __name__ == "__main__":
    params = checkArgs(sys.argv)

    if len(params):
        convertFile(params)
    
# End of sum-hours.py