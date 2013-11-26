from runTregex import Treebank as TB
from pdb import set_trace
from nltk.stem.wordnet import WordNetLemmatizer
from collections import Counter
from operator import itemgetter

lem = WordNetLemmatizer()


pat = "/VB[DN]/ , /(was|were|are|been|being)/"
corpus_dir = "/home/chase/CompLing/stanford-tregex-2012-03-09/treebank_3/parsed/mrg/wsj/"

#trees = TB(copus_dir, pat)
#trees.run()
all_inflected_verbs = []
cnt = Counter()
with open('verbs.txt', 'r') as fi:
    for line in fi:
        if line == '' or line == '\n':
            continue
        try: inflected_verb = line.split()[1][:-1].lower()
        except: set_trace()
        v = lem.lemmatize(inflected_verb, 'v')
        cnt[v] += 1
top_50 = map(lambda x: x[0],sorted([(x,cnt[x]) for x in cnt], key = itemgetter(1))[-50:])
print top_50
trees = TB(corpus_dir, pat)
trees.run()


passives=[]
for t in trees:
   # print t.matchTree.leaves()[0].lower()
    print lem.lemmatize(t.matchTree.leaves()[0].lower())
    
    if lem.lemmatize(t.matchTree.leaves()[0].lower()) in top_50:
        passives.append(t)
        print t.leaves()
print len(passives)
