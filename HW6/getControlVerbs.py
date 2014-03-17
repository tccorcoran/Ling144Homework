""" General approach: serach for control-type structures which may be ambigious (with raising)
then search for those verbs to see if they exist in "There[ex] VERB" contexts
e.g we find "John seems to be beside himself today"
    so we search for "/[tT]here/ . (/VB/ < /^(seem)/)"
    if this returns any results, "seem" must be a raising verb
"""

from pdb import set_trace
import runTregex as tx
from nltk.stem import PorterStemmer
ps = PorterStemmer()
treebank_dir = "/home/chase/CompLing/stanford-tregex-2012-03-09/treebank_3/parsed/mrg/wsj/"

unfiltered = set()
for t in trees:
    unfiltered.add(ps.stem_word(t.matchTree.leaves()[0]).lower())

# this takes forever and  isn't really too effective...
for word in unfiltered:
    pat = "(/[Tt]here/ > EX) . /^%s/"%word
    reload(tx) 
    trees = tx.Treebank(treebank_dir, pat)
    trees.run()
    if len(trees) > 0:
        print word

