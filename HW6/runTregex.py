#!/usr/env python

import subprocess
import json
from nltk.tree import ParentedTree
from pdb import set_trace

class SearchTree(ParentedTree):
    def loadMatches(self, e):
        self.e = e
        self.handles = {}
        self.handlePositions = {}
        self.filename = e["filename"]
        self.treenumber = e["treeNumber"]
        matchNumber = e["matchTreeNumber"] - 1
        self.matchTree = self.getTreeDepthFirstNumber(matchNumber)
        for handle,structure in e["nodes"].items():
            try:
                loc = int(structure["treeNumber"]) -1
                # NOTE: this doesn't deal with leaf handles, because they are strings; probably should stick with the tree positions...
                self.handles[handle] = self.getTreeDepthFirstNumber(loc)
                self.handlePositions[handle] = loc
            except:
                pass
    
    def getTreeDepthFirstNumber(self, num):
        return self[self.treepositions()[num]]
    
    def makeJSON(self, handles, position):
        out = {"name": self.node, "type": "nonterm" , "children": [], "position": position}

        # is this a handle, perhaps?
        for handle,treelet in handles.items():
            if treelet == self:
                out["handle"] = handle
                break
        
        
        for child in self:
            if isinstance(child, basestring): # is this a leaf?
                chOut,position = self.makeJSONleaf(child, handles, position+1)
            else:
                chOut,position = child.makeJSON(handles, position+1)
            out["children"].append(chOut)

        return (out, position)
    
    def makeJSONleaf(self, element, handles, position):
        out = {"name": element, "type": "term", "position": position}
    
        for handle,treelet in handles.items():
            if treelet == self:
                out["handle"] = handle
                break
        
        return (out, position)
class AnotherSearchTree(SearchTree):

    def adjacent(self, elt):
        """expects elt to a be a string"""
        #set_trace()
        root = self.root() # full tree
        def checkIsElt(node):
            if isinstance(node,str):
                if node == elt: return True
            else:
                if node.node == elt: return True
        if not isinstance(elt,str) and not isinstance(elt,unicode):
            print "Expected a string"
            return False

        if not self.right_sibling():
            # no right sibling, we have to find the next right branch to climb down
            node = self
            while node != root and not node.right_sibling():
                # search up tree for a right branch to follow down
                if checkIsElt(node): return True
                try: 
                    node = node.parent()
                except: # maybe we're at  root
                   print "erre"
                   break

            pos = node.right_sibling().treeposition()
            for _ in xrange(node.right_sibling().height()):
            # look at the left edge of the node
                try:
                    # something something better to ask forgiveness than 
                    # permission
                    node=root[pos]
                    pos += (0,) # get leftmost if exists, else we're at a leaf
                except (IndexError, TypeError):
                    break
                if checkIsElt(node): return True

        if not self.left_sibling():
            #check right edges of ancester with lowest left branch left sister
            node = self
            while node != root and not node.left_sibling():
                try:
                    node = node.parent()
                except: 
                    print "eerer"    
            pos = node.left_sibling().treeposition()
            for _ in xrange(node.left_sibling().height()):
                try:
                    node = root[pos]
                    pos += (len(node)-1,)
                except (IndexError, TypeError):
                    break
                if checkIsElt(node): return True

        if self.right_sibling():
            #check left sibling down
            node = self.right_sibling()
            pos = node.treeposition()
            if checkIsElt(node): return True
            for _ in xrange(node.height()):
                try: 
                    node = root[pos]
                    pos += (0,)
                except (IndexError, TypeError):
                    break
                if checkIsElt(node): return True
        if self.left_sibling():
            # look down the rightmost nodes of left sib
            node = self.left_sibling()
            rightest = (len(node) -1,)
            pos = node.treeposition()
            if checkIsElt(node): return True
            for _ in xrange(node.height()):
                try: 
                    node = root[pos+rightest]
                    rightest += (len(node)-1,)
                except (IndexError, TypeError):
                    break
                if checkIsElt(node): return True

class Treebank():

    javaJars = "/media/Preload/Documents and Settings/Chase Corcoran/My Documents/School/Ling. 144/repos/ComputationalMethods/scripts/*:/media/Preload/Documents and Settings/Chase Corcoran/My Documents/School/Ling. 144/repos/ComputationalMethods/scripts/stanford-tregex-2013-06-20/stanford-tregex.jar"
    
    javaPath = "/usr/bin/java"
    programLoc = "edu.ucsc.TregexWrapper.TregexWrapper"
    
    trees = []
    def __init__(self, dir, pattern, javaJars=None, javaPath=None):
        self.dir = dir
        self.pattern = pattern
        if javaJars:
            self.javaJars = javaJars

        if javaPath:
            self.javaPath = javaPath
        
    def run(self):
        print "Running tregex..."
        raw = subprocess.check_output(["java", "-cp", self.javaJars, self.programLoc, self.pattern, self.dir], stderr=subprocess.STDOUT)
        print "Processing output..."
        for ma in raw.split("\n"):
            try:
                m = json.loads(ma)
                tree = SearchTree(m["tree"])
            except:
                pass
            else:
                tree.loadMatches(m)
                self.trees.append(tree)
        print "Done!"
        print "%d matches found"%len(self.trees)
    def __getitem__(self, key):
        return self.trees[key]

    def __len__(self):
        return len(self.trees)

if __name__ == "__main__":
    dir = "/home/chase/CompLing/stanford-tregex-2012-03-09/treebank_3/parsed/mrg/wsj/"
    #pattern = "(/VB/ . (/TO|IN/ . /VB/))" 
    pattern = "/are/ . /VB[ND]/"
    t = Treebank(dir, pattern)
    t.run()
    for tree in t:
        print ' '.join(tree.leaves())
    print len(t)
    #print t[:]
