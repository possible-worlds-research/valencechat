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
        return self.frames[self.current_frame]

    def get_verbalisation(self, x, goal, attribute=None):
        #print("Getting verbalisation for",goal)
        if not attribute:
            templates = self.verbalisations[f'<{goal}>']
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
                goal = material
            elif next_step == 'new_context':
                curr = self.add_frame(material)
                goal = curr.sample_core_unfilled()
            elif next_step == 'new_belief_holder':
                goal = 'branchout:beliefholder'
        return goal

    def converse(self, concept):
        write_to_dir(f"CONCEPT: {concept}", self.data_dir, self.session_id)
        frame = Frame(name=concept)
        curr = self.add_frame(frame)
        goal = self.get_goal()
        question, counterfactual, explanation = self.get_verbalisation(concept, goal)
        write_to_dir(f"BOT >> {goal.upper()}: {question}", self.data_dir, self.session_id)
        user_input = input(f"BOT >> {question}\nHUM >> ").rstrip('\n')

        while user_input != 'q':
            write_to_dir(f"HUM >> {goal.upper()}: {user_input}", self.data_dir, self.session_id)
            frame.fill(goal, user_input)
            goal = self.get_goal()
            question, counterfactual, explanation = self.get_verbalisation(concept, goal)
            write_to_dir(f"BOT >> {goal.upper()}: {question}", self.data_dir, self.session_id)
            user_input = input(f"BOT >> {question}\nHUM >> ").rstrip('\n')


if __name__ == '__main__':
    session_id = datetime.now().strftime('%Y-%m-%d-%H:%M')
    chat = Chat(lang='en', session_id=session_id)
    chat.converse(sys.argv[1])
