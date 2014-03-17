import runTregex as TX
from pdb import set_trace
from nltk.stem.wordnet import WordNetLemmatizer
from collections import Counter
from operator import itemgetter

lem = WordNetLemmatizer()


pat = "(/VB[DN]/ , /^(was|were|are|been|being|be|'re)$/)"
corpus_dir = "/home/chase/CompLing/stanford-tregex-2012-03-09/treebank_3/parsed/mrg/wsj/"


def hasBy(tree):
    # yeah this is bad, but it kind of mostly works
#    set_trace()
    if 'by' in tree.leaves()[tree.leaves().index(tree.matchTree.leaves()[0]):]:
        return True
    return False
all_inflected_verbs = []
cnt = Counter()
with open('verbs.txt', 'r') as fi:
    
    for line in fi:
        if line == '' or line == '\n' or line.startswith('#'):
            continue
        try: inflected_verb = line.split()[1][:-1].lower()
        except: set_trace()
        v = lem.lemmatize(inflected_verb, 'v')
        cnt[v] += 1
top_50 = map(lambda x: x[0],sorted([(x,cnt[x]) for x in cnt], key = itemgetter(1))[-50:])
#print "Top 50 verbs"
#print '\n'.join(top_50)
trees = TX.Treebank(corpus_dir, pat)
trees.run()

passives=[]
by = Counter()
notBy = Counter()
for t in trees:
    #set_trace()  
    w =lem.lemmatize(t.matchTree.leaves()[0].lower(), 'v') 
    if w in top_50:
        if hasBy(t):
            by[w] += 1
        else:
            notBy[w] +=1
reload(TX)
pat = "pat = (/^VB/ !, /^(was|were|are|been|being|be|'re)$/)"
trees = TX.Treebank(corpus_dir,   pat)
trees.run()
active = Counter()
for t in trees:
    w =lem.lemmatize(t.matchTree.leaves()[0].lower(), 'v')
    if w in top_50:
        active[w] += 1
for w in top_50:
    if w not in by:
        by[w] = 0
    if w not in notBy:
        notBy[w] = 0
    if w not in active:
        active[w] = 0
print "      Word     Active   Passive no by   Passive by"
for w in top_50:
    print "%10s%10d%10d%10d"%(w,active[w],notBy[w],by[w])
set_trace()

