'''
Main program. Asking for reasons.
'''
import sys
from os import getcwd
from os.path import join
from pathlib import Path
from datetime import datetime
from random import shuffle, randint
from valencechat.loaders import load_verbalisations, make_higher_frames
from valencechat.logger import write_to_dir

class Chat:
  
    def __init__(self,lang=None, session_id=None):
        self.lang = lang
        self.session_id = session_id
        self.verbalisations = load_verbalisations(self.lang)
        self.higher_frames = make_higher_frames(self.verbalisations)
        self.data_dir = join(getcwd(),join('data',self.lang))
        Path(self.data_dir).mkdir(exist_ok=True, parents=True)


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

    def get_q(self, frame, qud=None):
        if qud:
            templates = [t for t in self.higher_frames[frame] if t[0] == qud]
        else:
            templates = self.higher_frames[frame]
        if len(templates) > 0:
            shuffle(templates)
            qud, attribute = templates[0]
            return qud, attribute
        return None, None

    def pop_goal(self, frame, goal, attribute):
        if attribute:
            self.higher_frames[frame].remove((goal, attribute))
        else:
            self.higher_frames[frame].remove((goal, None))

    def check_finish(self):
        if len(self.higher_frames['class']) == 0:
            return True
        return False

    def converse(self, concept):
        write_to_dir(f"CONCEPT: {concept}", self.data_dir, self.session_id)
        frame = 'class'
        qud= 'definition' #question under discussion
        goal = f"{frame}:{qud}"
        attribute = None
        question, counterfactual, explanation = self.get_verbalisation(concept, goal)
        self.pop_goal(frame, qud, attribute)
        write_to_dir(f"BOT >> {goal.upper()}: {question}", self.data_dir, self.session_id)
        user_input = input(f"BOT >> {question}\nHUM >> ").rstrip('\n')

        while user_input != 'q':
            write_to_dir(f"HUM >> {goal.upper()}: {user_input}", self.data_dir, self.session_id)
            if frame == 'class':
                if counterfactual == 1 and explanation == 1:
                    frame = ['counterfact', 'explanation'][randint(0,1)]
                elif counterfactual == 1:
                    frame = 'counterfact'
                elif explanation == 1:
                    frame = 'explanation'
                else:
                    frame = 'class'
                qud, attribute = self.get_q(frame, qud=qud)
            else:
                frame = 'class'
                qud, attribute = self.get_q(frame)
            goal = f"{frame}:{qud}"
            if qud:
                question, counterfactual, explanation = self.get_verbalisation(concept, goal, attribute=attribute)
                self.pop_goal(frame, qud, attribute)
                write_to_dir(f"BOT >> {goal.upper()}: {question}", self.data_dir, self.session_id)
                user_input = input(f"BOT >> {question}\nHUM >> ").rstrip('\n')
            if frame != 'class' and self.check_finish():
                write_to_dir(f"HUM >> {goal.upper()}: {user_input}", self.data_dir, self.session_id)
                goal = 'convention:thankyou'
                utterance, _, _ = self.get_verbalisation(concept, goal)
                write_to_dir(f"BOT >> {goal.upper()}: {utterance}", self.data_dir, self.session_id)
                print(f"BOT >> {utterance}")
                break


if __name__ == '__main__':
    session_id = datetime.now().strftime('%Y-%m-%d-%H:%M')
    chat = Chat(lang='en', session_id=session_id)
    chat.converse(sys.argv[1])
