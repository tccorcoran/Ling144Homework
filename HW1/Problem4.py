#!/usr/bin/env python

"""Creates a PigLatin generator."""

__author__ = 'chase'
__email__ = "chase@ucsc.edu"
__credits__ = ['from http://usefulenglish.ru/phonetics/practice-consonant-clusters']

def pigLatin(w):
    """
	this function handles pigLatin for word w

    Args:
		w: a word

    Returns:
        pigLatined: a PigLatin representation of word w

    Raises:
        Nothing

	"""
    vowels = 'aeiou'

    # from http://usefulenglish.ru/phonetics/practice-consonant-clusters
    consonant_clusters_bi = {'st','sp','sl','sh', 'sk', 'tr', 'fl', 'bl', 'br', 'tw','th', 'pl', 'pr',
                                 'sm', 'dr', 'cl', 'cr', 'gl', 'gr', 'sn', 'sw', 'dw', 'qu','gw'}

    consonant_clusters_tri = {'squ', 'str', 'spl', 'scr', 'thr', 'shr', 'squ'}


    if not isinstance(w, str):
        return w # make sure w is a string type
    if not w[0].isalpha():
        return w # make sure the string starts with a letter
    if len(w) == 1:
        if w in ('i','a'):
            return w + 'way'
        else:
            return w
    if len(w) > 3 and w[:3].lower() in consonant_clusters_tri:
        #
        ending = w[:3] + 'ay'
        rest = w[3:]
    elif len(w) > 2 and w[:2].lower() in consonant_clusters_bi:
        #
        ending = w[:2] + 'ay'
        rest = w[2:]
    elif w[0].lower() in vowels:
        #
        if w[-1] in vowels:
            rest = w[:-1]
        else:
            rest = w
        ending =  'way'
    else:
        ending = 'ay'
        rest = w[1:] + w[0]


    pigLatined = rest + ending

    return pigLatined

def pigLatinSentence(text):
    """
    this function handles pigLatin for all words in string S.

    Args:
    text: a string

    Returns:
       a string in pig latin

    Raises:
        Nothing

    """

    punct = {",", '.'}
    for p in punct:
        text = text.replace(p, ' %s '%p)

    pl_list = []
    for w in text.split():
        pl_list.append(pigLatin(w))

    pl_string = ' '.join(pl_list)
    for p in punct:
        pl_string = pl_string.replace(' '+p, p)

    return pl_string

if __name__ == "__main__":

    # all of the below code is used to TEST whether yours worked

    inputLine = "if you think, sadly, that he will actually visit, then I am fine."
    key = "ifway ouyay inkthay, adlysay, atthay ehay illway actuallyway isitvay, enthay I amway inefay."
    pg = pigLatinSentence(inputLine)
    if pg == key:
        result = "PASS"
    else:
        result = "FAIL"
    print inputLine
    print pg
    print result
