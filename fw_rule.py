#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import copy
# import socket

from common_func import *

# Parent class fw_rule: defines common atributes and methods
#
class fw_rule:
    def __init__(self, args = []):

        self.rule = {'id': 0,
                    'drt': 'in', 
                    'intf': 'wan',
                    'action': '', 
                    'proto': '', 
                    'src': {'addr': '', 'port': ('null', 'null')},
                    'dst': {'addr': '', 'port': ('null', 'null')}, 
                    'opts': [] }
        
        self.r_id = 0
        self.invalid = []
        self.to_replace = []
        self.intf_d = {'wan': 'wan'}
        self.drt = 'in'

        if len(args):
            self.drt, i_dct = args
            if len(i_dct):
                self.intf_d = i_dct


    def to_rule(self, lst):
        rule = copy.deepcopy(self.rule)
    
        self.r_id += 10
        rule['id'] = self.r_id

        return rule


    def from_rule(self, rule):
        rtr = 'Rule ' + str(rule['id'])

        return rtr


# Class acl: Converts rules to/from a Brocade/Ruckus ACL sintax
#
class acl(fw_rule):   
    header = lambda self, s = '': 'no ip access-list extended %s-%s\n!\nip access-list extended %s-%s\n!' % (self.intf_d.keys()[0], self.drt, self.intf_d.keys()[0], self.drt)
 
    footer = lambda self, s = '': '!\n! End of ACL %s-%s\n' % (self.intf_d.keys()[0], self.drt)

    def __init__(self, args = []):
        fw_rule.__init__(self, args)
        
        self.invalid = ['!', 'ip access-list', 'established', 'remark']     
        self.to_replace = [('\n', ''), ('host', '')]


    def gen_prt(self, ports):
        src_p_lo, src_p_hi = ports

        expr = ''
        if src_p_lo != 'null':
            if src_p_lo == src_p_hi:
                expr = ' eq ' + src_p_lo
            elif src_p_lo == '0':
                expr = ' lt ' + str(int(src_p_hi)+1)
            elif src_p_hi == '65535':
                expr = ' gt ' + str(int(src_p_lo)-1)
            else:
                expr = ' range ' + src_p_lo + ' ' + src_p_hi

        return expr


    def to_rule(self, lst):
        operators = { 'eq': lambda l: ((l[0], l[0]), 2), 
                      'lt': lambda l: (('0', str(int(l[0])-1)), 2), 
                      'gt': lambda l: ((str(int(l[0])+1), '65535'), 2),
                      'range': lambda l: ((l[0], l[1]), 3) }
        
        idx = 0
        lidx = len(lst) - 1

        rule = copy.deepcopy(self.rule)

        self.r_id += 10

        if lst[idx] == 'sequence':
            idx += 2

        rule['id'] = self.r_id
        rule['intf'] = self.intf_d.values()[0]
        rule['action'] = lst[idx]
        idx += 1
        rule['proto'] = lst[idx]
        idx += 1
        rule['src']['addr'] = add_32(lst[idx])
        idx += 1

        if lst[idx] in operators.keys():
            rule['src']['port'], jump = operators.get(lst[idx])(lst[idx+1:])
            idx += jump

        rule['dst']['addr'] = add_32(lst[idx])

        if idx < lidx:
            idx += 1
            if lst[idx] in operators.keys():
                rule['dst']['port'], jump = operators.get(lst[idx])(lst[idx+1:])
                idx += jump

            rule['opts'] = lst[idx:]
        
        return rule


    def from_rule(self, rule):
        act = rule['action']
        if act == 'match':
            act = '!' + act
        acl = ' ' + act + ' ' + rule['proto']
        acl += ' ' + rule['src']['addr']
        acl += self.gen_prt(rule['src']['port'])
        acl += ' ' + rule['dst']['addr']
        acl += self.gen_prt(rule['dst']['port'])

        if len(rule['opts']):
            acl += ' ' + ' '.join(rule['opts'])

        return acl


# Class csv: Converts rules to/from a CSV string
#
class csv(fw_rule):
    
    header = lambda self, s = '': 'Begin ACL %s\nId,Ação,Protocolo,Host de Origem,Porta de Origem,Host de Destino,Porta de Destino,Interface,Direção,Opções' % s

    footer = lambda self, s = '': 'End ACL %s\n' % s

    def __init__(self, args = []):
        fw_rule.__init__(self, args)

        self.invalid = ['Begin','End','Id']
        self.replace = []
        self.to_replace = [(' ','+'), (',-,', ',null-null,'), ('(', ''), (')',''), (',', ' '), ('\n', '')]


    def gen_prt(self, ports):
        src_p_lo, src_p_hi = ports

        if src_p_lo == src_p_hi:
            expr = src_p_lo
        else:
            expr = src_p_lo + '-' + src_p_hi
                    
        return expr


    def to_rule(self, lst):
        rule = copy.deepcopy(self.rule)

        # print lst

        self.r_id += 10
        
        rule['id'] = self.r_id     
        rule['action'] = lst[1]
        rule['proto'] = lst[2]
        rule['src']['addr'] = add_32(lst[3].split('+')[-1])
        rule['src']['port'] = prt_tuple(lst[4])
        rule['dst']['addr'] = add_32(lst[5].split('+')[-1])
        rule['dst']['port'] = prt_tuple(lst[6])
        rule['intf'] = lst[7]
        rule['drt'] = lst[8]
        rule['opts'] = '&'.join(lst[9:]).split('&')

        # print rule
        return rule

 
    def from_rule(self, rule):
        csv = str(rule['id']) + ',' + rule['action'] + ',' + rule['proto']
        csv += ',' + lookup(rule['src']['addr']) + ',' + self.gen_prt(rule['src']['port'])
        csv += ',' + lookup(rule['dst']['addr']) + ',' + self.gen_prt(rule['dst']['port'])
        csv += ',' + rule['intf'] + ',' + rule['drt']
        if len(rule['opts']):
            csv += ',' + '&'.join(rule['opts'])

        return csv


# Class pfsense: convert rules to/from the XML sintax used by pfSense
#
class pfsense(fw_rule):
    header = lambda self, s = '': xmltag(0, 'filter', '', 's')
    footer = lambda self, s = '': xmltag(0, 'filter', '', 'e')    

    def __init__(self, args = []):
        fw_rule.__init__(self, args)
        self.r_id_delta = int(time.strftime('%s'))
        self.act_d = {'permit': 'pass', 'deny': 'block', 'match': 'match'}

    def gen_prt(self, ports):
        src_p_lo, src_p_hi = ports

        if src_p_lo == src_p_hi:
            expr = src_p_lo
        else:
            expr = src_p_lo + '-' + src_p_hi
                    
        return expr


    def from_rule(self, rule):
        xml = xmltag(1,'rule', '', 's') + '\n'
        n_id = self.r_id_delta + rule['id']
        xml += xmltag(2,'tracker',str(n_id))
        xml += xmltag(2,'type',self.act_d[rule['action']])
        xml += xmltag(2,'interface',rule['intf'])
        xml += xmltag(2,'ipproto','inet')
        drt = rule['drt'].replace('both','any')
        xml += xmltag(2,'direction',drt)
        if drt != 'in' or rule['action'] == 'match':
            xml += xmltag(2,'quick','yes')
            xml += xmltag(2,'floating','yes')
        if rule['proto'] != 'ip':
        	xml += xmltag(2,'protocol',rule['proto'])
        xml += xmltag(2,'source','', 's') + '\n'
        if rule['src']['addr'] == 'any':
        	xml += xmltag(3,'any')
        else:
        	xml += xmltag(3,'address',del_32(rule['src']['addr']))
        port = self.gen_prt(rule['src']['port'])
        if port != 'null': xml += xmltag(3,'port',port)
        xml += xmltag(2,'source', '', 'e') + '\n'
        xml += xmltag(2,'destination', '', 's') + '\n'
        if rule['dst']['addr'] == 'any':
        	xml += xmltag(3,'any')
        else:
        	xml += xmltag(3,'address',del_32(rule['dst']['addr']))
        port = self.gen_prt(rule['dst']['port'])
        if port != 'null': xml += xmltag(3,'port',port)
        xml += xmltag(2,'destination', '', 'e') + '\n'
        if 'log' in rule['opts']: xml += xmltag(2,'log')
        xml += xmltag(1,'rule', '', 'e')

        return xml

# Class ipfw: convert rules to/from the sintax used by ipfw(8)
#
class ipfw(fw_rule):

    def __init__(self, args = []):
        fw_rule.__init__(self, args)

        self.invalid = [ '#' ]
        self.to_replace = [ ('{ ',''), (' }', ''), (' or ', '|'), 
                            ('{', ':'), ('}', ''), ('from',''), ('to',''), 
                            ('dst-port ', ''), ('src-port ', ''), ('setup', ''), ('via', ''),
                            ('allow', 'permit'), ('deny', 'deny'), ('count','match') ]


    def to_rule(self, lst):      
        idx = 1
        # intf_lst = ['em0', 'em1', 'igb0']
        opts = []


        rule = copy.deepcopy(self.rule)

        self.r_id += 10

        if 'log' in lst:
            opts.append('log')
            lst.remove('log')

        if 'in' in lst:
            rule['drt'] = 'in'
            lst.remove('in')
        elif 'out' in lst:         
            rule['drt'] = 'out'
            lst.remove('out')
        else:
            rule['drt'] = 'both'

        lidx = len(lst) - 1
        
        # print lst

        rule['id'] = self.r_id
        rule['action'] = lst[idx]
        idx += 1
        rule['proto'] = lst[idx]
        idx += 1
        rule['src']['addr'] = add_32(lst[idx])
        idx += 1

        if lst[idx].replace('-','').isdigit():
            rule['src']['port'] = prt_tuple(lst[idx])
            idx += 1

        rule['dst']['addr'] = add_32(lst[idx])
        idx += 1

        lst = lst[idx:]

        if len(lst):
            idx = 0
            if lst[idx].replace('-','').isdigit():
                rule['dst']['port'] = prt_tuple(lst[idx])
                lst = lst[1:]

            if len(lst):
                if lst[idx] in intf_d.keys():
                    rule['intf'] = intf_d[lst[idx]]
                    lst = lst[1:]
                
            opts.extend(lst)
        
        rule['opts'] = opts
        
        return rule
     

# Dummy main function
#
if __name__ == "__main__":
    pass

#
# End of fw_rule.py
#

