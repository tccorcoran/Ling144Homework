 #!/usr/bin/env python

"""Creates a PigLatin generator."""

__author__ = 'chase'
__email__ = "tcorcora@ucsc.edu"
__credits__ = ['http://usefulenglish.ru/phonetics/practice-consonant-clusters']

def pigLatin(w, d):
    """
    this function handles pigLatin for word w, for dialect d

    Args:
        w: a word
        d: a dialect (as a string)

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
        return w  # make sure w is a string type
    if not w[0].isalpha():
        return w  # make sure the string starts with a letter
    if len(w) == 1:
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
        ending = d
    else:
        if w[0].lower() in {'s'}:
            ending = 'ay'
        else:
            ending = d
        rest = w[1:] + w[0]


    pigLatined = rest + ending

    return pigLatined

if __name__ == "__main__":

    # all of the below code is used to TEST whether yours worked
    # a list of test word -> pg examples, as a dict
    wordsToPigLatin = {"artichoke": ("artichokyay", "yay"),
                       "stipple": ("ipplestay", "way"),
                       "123re": ("123re", "ay"),
                       "soup": ("oupsay", "way")}

    # per word, get the pg, the expected answer, and print success
    for word in wordsToPigLatin:
        ans, dialect = wordsToPigLatin[word]
        pg = pigLatin(word, dialect)
        if pg == ans:
            result = "PASS"
        else:
            result = "FAIL"
        print word, pg, result
