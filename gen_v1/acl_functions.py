#!/usr/bin/python

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


def ip_expand(ip_str):
    ips = []

    if '{' in ip_str:
        locts = []
        net, octs = ip_str.replace('}','').split('{')
        base = net.split('/')[0].split('.')
        for o in octs.split(','):
            if not '-' in o:
                locts.append(o)
            else:
                x, y = o.split('-')
                for r in range(int(x),int(y)+1):
                    locts.append(str(r))
        for l in locts:
            base[-1] = l
            ips.append('.'.join(base))
    else:
        ips.append(ip_str)

    return ips


def gen_ip_list(ip_lst_str):
    ip_lst = ip_lst_str.split('|')
    ips = []

    for ip in ip_lst:
        ips.extend(ip_expand(ip))

    return ips


def gen_port_list(prt_lst_str):
    port_lst = prt_lst_str.split(',')

    return port_lst


def prtxml(rule, ilist):
        flt = 1

	xmltag(1,'rule','','s')
	xmltag(2,'tracker',rule[9])
	xmltag(2,'type',rule[0])
        if rule[1] != 'null':
            if rule[1] in ilist.keys():
                iface = ilist[rule[1]]
            else:
                iface = rule[1]
	    xmltag(2,'interface',iface)
	xmltag(2,'ipprotocol','inet')
        if rule[3] == 'in':
            if rule[0] != 'match':
                flt = 0
	xmltag(2,'direction',rule[3])
        if flt == 1:
	    xmltag(2,'floating','yes')
	if rule[4] != 'ip':
	    xmltag(2,'protocol',rule[4])
	xmltag(2,'source','','s')
	src = rule[5]
	if src == 'any':
		xmltag(3,'any','')
	elif src == 'me':
		xmltag(3,'network','(self)')
	else:
		xmltag(3,'address',src)
	port = rule[6]
	if port != 'null': xmltag(3,'port',port)
	xmltag(2,'source','','e')
	xmltag(2,'destination','','s')
	dst = rule[7]
	if dst == 'any':
		xmltag(3,'any','')
	elif dst == 'me':
		xmltag(3,'network','(self)')
	else:
		xmltag(3,'address',dst)
	port = rule[8]
	if port != 'null': xmltag(3,'port',port)
	xmltag(2,'destination','','e')
        if rule[2] == 1: xmltag(2,'log','')
	xmltag(1,'rule','','e')

#
# End of acl-functions.py
#
