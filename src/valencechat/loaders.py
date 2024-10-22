from os.path import join, dirname, realpath, abspath
from pathlib import Path
import inspect

def load_verbalisations(lang):
    '''
    Convention file should be in format
    goal|bot answer.
    '''
    verbalisations = {}
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = dirname(abspath(filename))
    with open(join(path, "static", lang, "verbalisations.txt"), encoding='utf-8') as f:
        for l in f:
            if '|' not in l:
                continue
            l = l.rstrip('\n')
            goal, utterance, counterfactual, explanation = l.split('|')
            if goal in verbalisations:
                verbalisations[goal].append((utterance.strip(), int(counterfactual), int(explanation)))
            else:
                verbalisations[goal] = [(utterance.strip(), int(counterfactual), int(explanation))]
    return verbalisations


def make_higher_frames(verbalisations):
    '''
    Build basic conceptual frames from verbalisations.
    '''
    higher_frames = {}
    for typ in list(verbalisations.keys()):
        typ = typ[1:-1] #strip <>
        els = typ.split(':')
        frame = els[0]
        core = els[1]
        if len(els) > 2:
            attribute = els[2]
        else:
            attribute = None
        if frame in higher_frames:
            higher_frames[frame].append((core, attribute))
        else:
            higher_frames[frame] = [(core, attribute)]
    return higher_frames



