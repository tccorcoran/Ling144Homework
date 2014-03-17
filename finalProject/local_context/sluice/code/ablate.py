#env python
# create feature files for ablation tests
from pdb import set_trace
import getFeatures as gf
tags  = {"CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "MD", 
        "NN", "NNP", "NNPS", "NNS", "of", "PDT", "POS", "PRP", "?", "punc",
        "RB", "RBR", "RBS", "RP", "TO", "UH", "VB", "VBG", "VBN", "VBP",
        "VBZ", "WDT", "WP", "WRB", "sym", "2", ".", ":", ",", "*"}

folders = {"DEV": "../dev", "TRAIN": "../combined"}
for folder in folders:
    for tag in tags:
#        set_trace()
        out_file = "%s-%s.dat"%(folder,tag)
        gf.disallowed_tags = {tag}
        gf.run([None,folders[folder],out_file])
