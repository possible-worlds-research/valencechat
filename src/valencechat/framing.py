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

        # Definition for the concept, cases where the definition might not apply,
        # why this is a good definition.
        self.definition = {'surface_form':'', 'explanation':'', 'counterfactuals':[]}

        # Instances for the concept: a list of objects of class Frame
        self.instances = []

        # Valence for the concept, cases where the valence would be different,
        # why this is a good definition.
        self.valence = {'score':0.0, 'explanation':'', 'counterfactuals':[]}

        # Prevalence for the concept, cases where the valence would be different,
        # why this is a good definition.
        self.prevalence = {'score':0.0, 'explanation':'', 'counterfactuals':[]}

        # Labels for each slot in the frame
        self.labels = {
                'definition:surface_form': self.definition['surface_form'],
                'definition:explanation': self.definition['explanation'],
                'definition:counterfactuals': self.definition['counterfactuals'],
                'instances': self.instances,
                'valence:score': self.valence['score'],
                'valence:explanation': self.valence['explanation'],
                'valence:counterfactuals': self.valence['counterfactuals'],
                'prevalence:score': self.prevalence['score'],
                'prevalence:explanation': self.prevalence['explanation'],
                'prevalence:counterfactuals': self.prevalence['counterfactuals'],
                }
                

        # Show the variables that should be filled in the core script.
        # By default, individuals do not have valence and prevalence.
        self.core_script = ['definition:surface_form', 'instances']
        if not self.individual:
            self.core_script.extend(['valence:score', 'prevalence:score'])

        # Show the variables that should remain unfilled in the core script.
        # By default, individuals have most labels blocked.
        self.blocked = []
        if self.individual:
            blocked = list(set(self.labels.keys()) - set(self.core_script))
            self.blocked.extend(blocked)

        # Placeholder to hold the list of filled frame elements.
        self.filled = []

    def fill(self, label, value):
        if label != 'instances' and not label.endswith('counterfactuals'):
            self.labels[label] = value
        else:
            self.labels[label].append(value)
        self.filled.append(label)

    def explore_from_frame(self, verbose=False):
        '''
        Engage in exploration from this frame. This could be by filling in some 
        non-essential slot of the current frame, or by branching out
        to some new context or belief holder.
        '''
        if verbose:
            print("Trying to sample non core unfilled.")
        non_core = self.sample_non_core_unfilled()
        if non_core:
            return 'sampled_non_core', non_core
       
        if verbose:
            print("Trying to sample new context.")
        context = self.pick_new_context()
        if context:
            # We assume the new frame is about the same ontological type as the parent (individual or concept)
            # This is perhaps a bit of a stretch...?
            new_frame = Frame(name=context, belief_holder=self.belief_holder, individual=self.individual)

            # Contexts are not particularly easily 'defined'
            new_frame.core_script.remove('definition:surface_form')

            # Redefine blocked list is not needed anymore, as the number of arguments will select for the right verbalisations.
            del new_frame.blocked[:]
            return 'new_context', new_frame

        if verbose:
            print("Trying to sample new belief holder")
        new_frame = Frame(name=self.name, belief_holder=None, individual=self.individual)
        return 'new_belief_holder', new_frame

    def pick_new_context(self):
        '''
        This picks a context of interest to build a new frame.
        'Context' here could refer to a particular instance, or
        to a counterfactual context.
        '''
        contexts = []
        contexts.extend(self.instances)
        contexts.extend(self.valence['counterfactuals'])
        contexts.extend(self.prevalence['counterfactuals'])
        shuffle(contexts)
        #print("Possible new contexts",contexts)
        context = f"{self.name}:{contexts[0]}"
        return context

    def sample_core_unfilled(self):
        '''
        Sample from frame elements from core script that are 
        currently unfilled.
        '''
        core_unfilled = list(set(self.core_script) - set(self.filled) - set(self.blocked))
        if len(core_unfilled) > 0:
            shuffle(core_unfilled)
            return core_unfilled[0]
        return None

    def sample_non_core_unfilled(self):
        '''
        Sample from frame elements from non-core elements that are 
        currently unfilled.
        '''
        unfilled = list(set(self.labels.keys()) - set(self.filled) - set(self.blocked))
        if len(unfilled) > 0:
            shuffle(unfilled)
            return unfilled[0]
        return None

    def jsonify(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4) 

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


