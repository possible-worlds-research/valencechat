from os.path import join, dirname, realpath, abspath
from pathlib import Path
import inspect

def parse_verbalisations(verbalisations, goal, arity, individual, attribute):
    templates = []
    tmp_verbalisations = verbalisations.copy()
    pattern = '<'
    if individual:
        pattern+='individual:'
    else:
        pattern+='concept:'
    pattern+=goal
    if attribute:
        pattern+=':'+attribute
    pattern+='>'
    if not attribute:
        for k,v in verbalisations.items():
            tmp_k = ':'.join(k.split(':')[:-1])+'>'
            tmp_verbalisations[tmp_k] = v
    if pattern in tmp_verbalisations:
        templates = tmp_verbalisations[pattern]
    print("PARSE PATTERN",pattern,"POSSIBLE TEMPLATES",templates)
    if arity == 1:
        templates = [t for t in templates if '<y>' not in t and '<z>' not in t]
    if arity == 2:
        templates = [t for t in templates if '<y>' in t and '<z>' not in t]
    if arity == 3:
        templates = [t for t in templates if '<z>' in t]
    print("PARSER FINAL TEMPLATES",templates)
    return templates
