'''
Main program. Asking for reasons.
'''
import sys
from os import getcwd
from os.path import join
from pathlib import Path
from datetime import datetime
from random import shuffle, randint
from valencechat.loaders import load_verbalisations
from valencechat.parsers import parse_verbalisations
from valencechat.logger import write_to_dir
from valencechat.framing import Frame

class Chat:
  
    def __init__(self,lang=None, session_id=None):
        self.lang = lang
        self.session_id = session_id
        self.verbalisations = load_verbalisations(self.lang)
        self.frames = []
        self.current_frame = None
        self.data_dir = join(getcwd(),join('data',self.lang))
        Path(self.data_dir).mkdir(exist_ok=True, parents=True)

    def add_frame(self, frame):
        self.frames.append(frame)
        self.current_frame = len(self.frames) - 1

    def get_frame_by_name(self, name):
        curr = None
        frame = None
        for i,f in enumerate(self.frames):
            if f.name == name:
                curr = i
                frame = f
                break
        return curr, frame

    def get_verbalisation(self, goal, args, individual=False, attribute=None):
        #print("Getting verbalisation for",goal)
        verbalisation = None
        arity = len(list(filter(None, args)))
        templates = parse_verbalisations(self.verbalisations, goal, arity, individual, attribute)
        if len(templates) > 0:
            shuffle(templates)
            template = templates[0]
            # For the minute, accept up to three arguments
            args = {'<x>': args[0], '<y>': args[1], '<z>': args[2]}
            for var, val in args.items():
                if val:
                    template = template.replace(var, val)
            verbalisation = template
        return verbalisation

    def get_goal(self):
        frame = self.frames[self.current_frame]
        goal = frame.sample_core_unfilled()
        print("Sampled core:",goal)
        if not goal:
            next_step, material = frame.explore_from_frame()
            if next_step == 'sampled_non_core':
                goal = material
                print("Sampled non core:",goal)
            elif next_step == 'new_context':
                self.add_frame(material)
                goal = self.frames[self.current_frame].sample_core_unfilled()
                print("Sampled new context:", goal)
            elif next_step == 'new_belief_holder':
                #print("Sampling new belief holder.")
                goal = 'branchout:beliefholder'
        return goal

    def get_question(self):
        c = 0
        goal = None
        question = None
        while c < 10 and not question: 
            goal = self.get_goal()
            curr = self.current_frame
            concept = self.frames[curr].name
            print("Attempting to ask about",concept)
            # For the minute, accept up to three arguments
            args = [None, None, None]
            splits = concept.split(':')
            splits = splits[:min(len(splits),3)]
            for i,el in enumerate(splits):
                args[i] = el
            args = args[:3]
            individual = self.frames[curr].individual
            question = self.get_verbalisation(goal, args, individual=individual)
            c+=1
        return goal, question

    def memorise_answer(self, goal, answer, verbose=False):
        print("Filling goal",self.frames[self.current_frame].name, goal)
        self.frames[self.current_frame].fill(goal, answer)
        if verbose:
            print(self.frames[self.current_frame].jsonify())

    def converse(self, concept, individual=False):
        write_to_dir(f"CONCEPT: {concept}", self.data_dir, self.session_id)
        frame = Frame(name=concept, individual=individual)
        self.add_frame(frame)
        goal, question = self.get_question()
        write_to_dir(f"BOT >> {goal.upper()}: {question}", self.data_dir, self.session_id)
        user_input = input(f"BOT >> {question}\nHUM >> ").rstrip('\n')

        while user_input != 'q':
            write_to_dir(f"HUM >> {goal.upper()}: {user_input}", self.data_dir, self.session_id)
            self.memorise_answer(goal, user_input)
            goal, question = self.get_question()
            if not question:
                print("BOT >> Thank you very much.")
                break
            write_to_dir(f"BOT >> {goal.upper()}: {question}", self.data_dir, self.session_id)
            user_input = input(f"BOT >> {question}\nHUM >> ").rstrip('\n')


if __name__ == '__main__':
    session_id = datetime.now().strftime('%Y-%m-%d-%H:%M')
    chat = Chat(lang='en', session_id=session_id)
    chat.converse(sys.argv[1])
