import os
import re
from glob import glob

def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s
     
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
    
def load_text(path):
    with open(path, 'r') as f:
        x = f.readlines()
    utt = x[0]
    # replace special tokens with question marks
    if '<DIA>' in utt:
        utt = utt.replace('<DIA>', '-')
    if '<UKN>' in utt:
        utt = utt.replace('<UKN>', '___')    
    return utt

def list_files(path, ext='svg'):
    result = [y for x in os.walk(path)
              for y in glob(os.path.join(x[0], '*.%s' % ext))]
    return result