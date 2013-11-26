""" General approach: serach for command type structures which may be ambigous (with raising)
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
#pattern = 'VP < (/VB/ . (TO . /VB/))'
pattern = "(/VB/ . (/TO|IN/ . /VB/))"
trees = tx.Treebank(treebank_dir, pattern)
trees.run()

unfiltered = set()
for t in trees:
    unfiltered.add(ps.stem_word(t.matchTree.leaves()[0]).lower())
set_trace()



