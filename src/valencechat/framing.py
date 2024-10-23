import numpy as np


class Frame:
  
    def __init__(self):
        '''
        A frame contains important information about some concept X.
        A concept can be something very generic ('cat', 'freedom')
        of very ad hoc ('the way people stand in front of other 
        people's bookshelves'). But it includes the following:
        - A definition for X.
        - A valence score (is X good or bad?)
        - A prevalence score (is X frequent or rare?)
        - Instances of the concept (vaguely defined, could either be
        an actual singular individual, or a contextualised version of
        the concept.)

        In addition, for definition, valence and prevalence, some 
        explanation and counterfactuals can be provided.

        The minimal script indicates which information must have been
        acquired for the frame to be considered minimally filled.
        '''

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

        # This is a little hacky. Show the variables that should be filled in the
        # minimal script, and their defaults.
        self.minimal_script = [
                (self.definition['surface_form'],''),
                (self.instances,[]),
                (self.valence['score'], 0.0),
                (self.prevalence['score'], 0.0),
                ]


    def check_minimal_script_filled(self):
        minimal_okay = True
        for condition in self.minimal_script:
            if condition[0] == condition[1]:
                minimal_okay = False
        return minimal_okay


    def get_unfilled(self):
        '''
        Return frame elements that are currently
        unfilled.
        '''
        print("Checking unfilled frame elements")


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


