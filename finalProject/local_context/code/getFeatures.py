#!/usr/bin/env python
from __future__ import print_function
from operator import itemgetter
from pdb import set_trace
from Header import Header
from collections import Counter
from glob import iglob
from nltk.tree import ParentedTree
import sys
#set_trace()
header = Header()
disallowed_tags = {}
whItems = {'that','who','what','when','where','why','how','which',
            'whose','whom','whoever','whomever','wherever',
            'whenever','whatever'}
def warning(*objs):
    print("getFeatures.py: WARNING: ", *objs, file=sys.stderr)

def getLocalContext(pos_leaf):
    d ={}
#    set_trace()
    for i,pos in enumerate(pos_leaf):
#        set_trace()
        word = pos[1]
        tag = pos[0]
        if tag in disallowed_tags: continue
        if word.lower() in whItems:
            header.add(word+'0')
            d[header[word+'0']] = 1
            leng = len(leaves)
            for j in [-3,-2,-1,1,3]: # num words to l and r
                if i+j < 0 or  i+j >= leng : continue
                try:
                    header.add(leaves[i+j]+str(j))
                    d[header[leaves[i+j]+str(j)]] = 1
                except IndexError:
                    set_trace()
    #if not d and 'macros' not in leaves: set_trace()
    return d

def makeRow(cnt, fileName):
    """Make a row in SMVlight format aka sparse vector
    e.g. -1 6:4 9:1 167:1 399:1 5573:1 27314:1 35300:1
    label := -1
    featrue id := 6 9 167 399 ...
    feature value := 1 1 1 1 ...
    feature ids always increase
    """
    if fileName[-2:] == 'SL': # sluice positive files end in SL 
        label = '1 '
    else:
        label = '-1 '
    # sort feat ids montonically inceasing
    return label + ' '.join(["%s:%d"%(k[0],k[1]) for k in 
                        sorted(cnt.items(),key=lambda x: int(x[0]))]) + '\n'


def gen(files):
    for f in files:
        with open(f) as fi:
            #set_trace()
            #leaves = ParentedTree.parse(fi.read()).leaves()
            pos = ParentedTree.parse(fi.read()).pos()
        yield makeRow(getLocalContext(pos), f)

def run(arg=sys.argv):
    if len(disallowed_tags) == 0: warning("Using all tags")

    if len(arg) == 3:
        files = iglob(arg[1]+"/*")
        print ("reading files from %s\n",arg[1])
        print ("writing to %s\n", arg[2])
        out_file = arg[2] 
    else:
        warning("Usage: getFeatures.py dir_in file_out.dat")
        exit(1)
    with open(out_file, 'w') as fo:
#    set_trace()
        for row in gen(files):
            fo.write(row)


if __name__ == "__main__":
    run()
