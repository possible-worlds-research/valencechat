from random import shuffle
import numpy as np
import json

class Frame:
  
    def __init__(self, name=None, belief_holder=None, individual=False):
        '''
        A frame contains important information about some concept X.
        A concept can be something very generic ('cat', 'freedom')
        of very ad hoc ('the way people stand in front of other 
        people's bookshelves'). But it includes the following:
        - The belief holder for the frame.
        - A name for X.
        - A definition for X.
        - A valence score (is X good or bad?)
        - A prevalence score (is X frequent or rare?)
        - Instances of the concept (vaguely defined, could either be
        an actual singular individual, or a contextualised version of
        the concept.)

        In addition, for definition, valence and prevalence, some 
        explanation and counterfactuals can be provided.

        The core script indicates which information must have been
        acquired for the frame to be considered corely filled.
        '''

        self.belief_holder = belief_holder
        self.name = name
        self.individual = individual
        self.definition = Definition()
        self.valence = Valence()
        self.prevalence = Prevalence()

        # Instances for the concept: a list of objects of class Frame
        self.instances = []


        # Labels for each slot in the frame
        self.labels = {
                'definition:surface_form': self.definition.set_surface_form,
                'definition:explanation': self.definition.set_explanation,
                'definition:counterfactuals': self.definition.set_counterfactuals,
                'valence:surface_form': self.valence.set_surface_form,
                'valence:score': self.valence.set_score,
                'valence:explanation': self.valence.set_explanation,
                'valence:counterfactuals': self.valence.set_counterfactuals,
                'prevalence:surface_form': self.prevalence.set_surface_form,
                'prevalence:score': self.prevalence.set_score,
                'prevalence:explanation': self.prevalence.set_explanation,
                'prevalence:counterfactuals': self.prevalence.set_counterfactuals,
                'instances': self.instances,
                }
                

        # Placeholder for the variables that should be filled in the core script.
        # By default, individuals do not have valence and prevalence.
        self.core_script = ['definition:surface_form', 'instances']
        if not self.individual:
            self.core_script.extend(['valence:surface_form', 'prevalence:surface_form'])

        # Placeholder the variables that should remain unfilled in the core script.
        # By default, individuals have most labels blocked.
        # Floats (scores) are blocked because filled automatically given the surface form.
        self.blocked = []
        for label,v in self.labels.items():
            if isinstance(v,float):
                self.blocked.append(label)
        if self.individual:
            blocked = list(set(self.labels.keys()) - set(self.core_script))
            self.blocked.extend(blocked)

        # Placeholder to hold the list of filled frame elements.
        self.filled = []
        
        # Placeholder to hold the list of filled frame elements that accept further input.
        self.optional = []

    # Add a value to a label. Mark the slot as filled if type is not list.
    def fill(self, label, value):
        if label == 'instances':
            self.labels[label].append(value)
            self.optional.append(label)
        else:
            r = self.labels[label](value)
            if isinstance(r,list):
                self.optional.append(label)
        self.filled.append(label)
        self.optional = list(set(self.optional))
        self.filled = list(set(self.filled))


    def return_sampled_non_core(self, verbose=False):
        if verbose:
            print("Trying to sample optional and non core unfilled.")
        non_core = self.sample_non_core_unfilled()
        return 'sampled_non_core', non_core


    def return_sampled_new_context(self, verbose=False):
        new_frame = None
        if verbose:
            print("Trying to sample new context.")
        context = self.sample_new_context()
        if context:
            # We assume the new frame is about the same ontological type as the parent (individual or concept)
            # This is perhaps a bit of a stretch...?
            new_frame = Frame(name=context, belief_holder=self.belief_holder, individual=self.individual)

            # Contexts are not particularly easily 'defined'
            new_frame.core_script.remove('definition:surface_form')

            # Redefine blocked list is not needed anymore, as the number of arguments will select for the right verbalisations.
            del new_frame.blocked[:]
        return 'new_context', new_frame


    def return_belief_holder(self, verbose=False):
        if verbose:
            print("Trying to sample new belief holder")
        new_frame = Frame(name=self.name, belief_holder=None, individual=self.individual)
        return 'new_belief_holder', new_frame


    def explore_from_frame(self, verbose=False):
        '''
        Engage in exploration from this frame. This could be by filling in some 
        non-essential slot of the current frame, or by branching out
        to some new context or belief holder.
        '''

        sampled_type, info = self.return_sampled_non_core(verbose=verbose)
        if info:
            return sampled_type, info

        sampled_type, info = self.return_sampled_new_context(verbose=verbose)
        if info:
            return sampled_type, info

        sampled_type, info = self.return_belief_holder(verbose=verbose)
        if info:
            return sampled_type, info


    def sample_new_context(self):
        '''
        This picks a context of interest to build a new frame.
        'Context' here could refer to a particular instance, or
        to a counterfactual context.
        '''
        contexts = []
        contexts.extend(self.instances)
        contexts.extend(self.valence.attributes['counterfactuals'])
        contexts.extend(self.prevalence.attributes['counterfactuals'])
        shuffle(contexts)
        #print("Possible new contexts",contexts)
        context = f"{self.name}:{contexts[0]}"
        return context

    def sample_optional(self):
        '''
        Sample from frame elements that accept several values.
        '''
        shuffle(self.optional)
        return self.optional[0]

    def sample_core_unfilled(self):
        '''
        Sample from frame elements from core script that are 
        currently unfilled.
        '''
        core_unfilled = list(set(self.core_script) - set(self.filled) - set(self.blocked))
        #print("Core unfilled",core_unfilled)
        if len(core_unfilled) > 0:
            shuffle(core_unfilled)
            return core_unfilled[0]
        return None

    def sample_non_core_unfilled(self):
        '''
        Sample from frame elements from non-core elements that are 
        currently unfilled.
        '''
        unfilled = list(set(self.labels.keys()) - set(self.filled) - set(self.blocked)) + self.optional
        #print("Non core unfilled",unfilled)
        if len(unfilled) > 0:
            shuffle(unfilled)
            return unfilled[0]
        return None

    def jsonify(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4) 


class Definition:
    '''
    Definition for the concept, cases where the definition might not apply,
    why this is a good definition.
    '''
    def __init__(self):
        self.attributes = {'surface_form':'', 'explanation':'', 'counterfactuals':[]}
    
    def set_surface_form(self, v):
        self.attributes['surface_form'] = v
        return self.attributes['surface_form']
    
    def set_explanation(self, v):
        self.attributes['explanation'] = v
        return self.attributes['explanation']
    
    def set_counterfactuals(self, v):
        self.attributes['counterfactuals'].append(v)
        return self.attributes['counterfactuals']


class Valence:
    '''
    Valence for the concept, corresponding score, cases where the valence 
    would be different, why this is a good judgment.
    '''
    def __init__(self):
        self.attributes = {'surface_form':'', 'score':0.0, 'explanation':'', 'counterfactuals':[]}
    
    def set_surface_form(self, v):
        self.attributes['surface_form'] = v
        return self.attributes['surface_form']
    
    def set_score(self, v):
        self.attributes['score'] = v
        return self.attributes['score']
    
    def set_explanation(self, v):
        self.attributes['explanation'] = v
        return self.attributes['explanation']
    
    def set_counterfactuals(self, v):
        self.attributes['counterfactuals'].append(v)
        return self.attributes['counterfactuals']


class Prevalence(Valence):
    '''
    Prevalence for the concept, corresponding score, cases where the valence 
    would be different, why this is a good judgment.
    '''
    pass



class Space:
    '''
    The space will hold everything that the bot knows.
    It has a basis in n (potentially labelled) dimensions.
    It has goals, which are locations in the (sub)space that the
    bot tends toward to, given its higher purpose.
    Concepts are simply points in space, in the usual fashion.
    '''

    def __init__(self, basis=None, goals=None):
        self.basis = basis
        self.goals = goals
        self.concepts = []

    def find_most_achievable_goal(self, concept=None):
        '''
        For a given concept (vector), compute distance
        to goals and return most achievable goal, together
        with vector showing the direction of the goal.
        '''
        print(f"Finding the most achievable goal for {concept.name}.")


class Goal:
    '''Location in a subspace of a space that we would like
    to be in. Defined by the subspace and the actual location.
    '''

    def __init__(self, subspace=None, destination=None):
        self.subspace = subspace
        self.destination = destination


class Concept:

    def __init__(self, name=None, belief_holder=None, stage=None, vector=None):
        '''
        A concept is basically a vector in some dimensionality.
        In addition, the vector is associated with some meta information:
        - a name (the surface form linked to it);
        - a belief holder (the individual for whom the concept is in that location;
        - a stage (as in, stage-level predicate).
        '''
        self.name = name
        self.belief_holder = belief_holder
        self.stage = stage
        self.vector = vector


class BeliefHolder:

    def __init__(self, name=None, entity=True):
        self.name = name
        self.entity = entity


