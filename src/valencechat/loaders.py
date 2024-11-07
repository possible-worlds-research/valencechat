from os.path import join, dirname, realpath, abspath
from pathlib import Path
import inspect

def load_verbalisations(lang, verbalisation_path=None):
    '''
    Convention file should be in format
    goal|bot answer.
    '''
    verbalisations = {}
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = dirname(abspath(filename))
    if not verbalisation_path:
        verbalisation_path = join(path, "static", lang, "verbalisations.txt")
    with open(verbalisation_path, encoding='utf-8') as f:
        for l in f:
            if '|' not in l:
                continue
            l = l.rstrip('\n')
            goal, utterance = l.split('|')
            if goal in verbalisations:
                verbalisations[goal].append(utterance.strip())
            else:
                verbalisations[goal] = [utterance.strip()]
    return verbalisations

