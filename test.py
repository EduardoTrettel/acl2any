#!/usr/bin/python
# -*- coding: utf-8 -*-

class l_one(object):
    rule = {'id': 0, 'tag': 'null'}

    def __init__(self):
        self.rule['id'] = 1

    def show(self):
        print self.rule

class l_two(l_one):
    def __init__(self):
        pass
        #super(l_one, self).__init__()
        # self.rule = l_one.rule
        #self.rule['id'] = 2

    
class l_3():
    rule = {'id': 0, 'tag': 'null'}

    def __init__(self):
        pass

    def one(self):
        def two(self, x):
            return x + 2

tabs = ( '\t', '\t', '\t', '\t', '\t')

ntabs = lambda x: ''.join(['\t'] * x)

xmltag = lambda x, s1, s2: ntabs(x) + '<%s>%s<\%s>' % (s1, s2, s1)
ml_xmltag = lambda x, s1, s_e: ntabs(x) + '<%s>' % s1 if s_e == 's' else ntabs(x) + '<\%s>' % s1


if __name__ == "__main__":
    #l1 = l_one()

    #l1.show()
    # l1.show()

    # l2 = l_two()
    # l2.show()

    # l3 = l_3()

    # print l3.one()

    print ml_xmltag(0,'filter', 's')
    print xmltag(2,'rule','0')
    print ml_xmltag(0,'filter', 'e')
