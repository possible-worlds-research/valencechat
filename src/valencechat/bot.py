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

    def get_verbalisation(self, x, goal, attribute=None):
        #print("Getting verbalisation for",goal)
        if not attribute:
            keys = [v for v in list(self.verbalisations.keys()) if v.startswith(f'<{goal}')]
            templates = []
            for k in keys:
                templates.extend(self.verbalisations[k])
        else:
            templates = self.verbalisations[f'<{goal}:{attribute}>']
        shuffle(templates)
        template = templates[0]
        verbalisation = template[0].replace('<x>', x)
        counterfactual = template[1]
        explanation = template[2]
        return verbalisation, counterfactual, explanation

    def get_goal(self):
        frame = self.frames[self.current_frame]
        goal = frame.sample_core_unfilled()
        if not goal:
            next_step, material = frame.explore_from_frame()
            if next_step == 'sampled_non_core':
                print("Sampling non core.")
                goal = material
            elif next_step == 'new_context':
                print("Sampling new context.")
                self.add_frame(material)
                goal = self.frames[self.current_frame].sample_core_unfilled()
            elif next_step == 'new_belief_holder':
                print("Sampling new belief holder.")
                goal = 'branchout:beliefholder'
        print("NEW GOAL", goal)
        return goal

    def get_question(self):
        goal = self.get_goal()
        curr = self.current_frame
        concept = self.frames[curr].name
        question, _, _ = self.get_verbalisation(concept, goal)
        return goal, question

    def memorise_answer(self, goal, answer):
        self.frames[self.current_frame].fill(goal, answer)
        print(self.frames[self.current_frame].jsonify())

    def converse(self, concept):
        write_to_dir(f"CONCEPT: {concept}", self.data_dir, self.session_id)
        frame = Frame(name=concept)
        self.add_frame(frame)
        goal, question = self.get_question()
        write_to_dir(f"BOT >> {goal.upper()}: {question}", self.data_dir, self.session_id)
        user_input = input(f"BOT >> {question}\nHUM >> ").rstrip('\n')

        while user_input != 'q':
            write_to_dir(f"HUM >> {goal.upper()}: {user_input}", self.data_dir, self.session_id)
            self.memorise_answer(goal, user_input)
            goal, question = self.get_question()
            write_to_dir(f"BOT >> {goal.upper()}: {question}", self.data_dir, self.session_id)
            user_input = input(f"BOT >> {question}\nHUM >> ").rstrip('\n')


if __name__ == '__main__':
    session_id = datetime.now().strftime('%Y-%m-%d-%H:%M')
    chat = Chat(lang='en', session_id=session_id)
    chat.converse(sys.argv[1])
