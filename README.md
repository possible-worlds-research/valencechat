# ValenceChat

This module implements an Eliza-like chatbot that will question the user about a concept and subsequently analyse its valence (i.e. whether the concept is positive or negative). The bot is being developed in English and German at this stage. This can be used to start teaching specific concepts to tiny chatbots trained from scratch, for instance by mixing ValenceChat utterances with a tiny Transformer output.

More in depth: the backend of the bot implements a basic ontological structure not unlike frames, which is filled as the human speaks to the bot. The ontology is meant to integrate counterfactuals, explanations and a notion of belief holders, so that a decent formalisation of the concept can eventually be achieved.

NB: This is work in progress. We will update this page as functionalities are developed. For the moment, the basic ontology is there, as well as the chat module. No analysis of the speaker's utterances are performed yet.

## Installation

We recommend installing this package in a virtual environment. If you do not have virtualenv installed, you can get it in the following way: 

```
sudo apt update
sudo apt install python3-setuptools
sudo apt install python3-pip
sudo apt install python3-virtualenv
```

Then, create a directory for ValenceChat, make your virtual environment and install the package:

```
mkdir valencechat
cd valencechat
virtualenv env && source env/bin/activate
pip install git+https://github.com/possible-worlds-research/valencechat.git
```

Just like Eliza, the module uses hard-coded utterances to interact with the human. Those can be found in the *src/valencechat/static/* directory, for English and German. You can change the utterances already included in the package, or add your own. We will add instructions here in the future to guide users through the process.

## Basic usage

The module can be used in a python program. Here is a basic example to run a conversation in German about the concept of sleep (*'Schlaf'*):

```
from datetime import datetime
from valencechat.bot import Chat
  
session_id = datetime.now().strftime('%Y-%m-%d-%H:%M')
chat = Chat('de', session_id)
chat.converse('Schlaf', individual=False)
```

When running this program, a chat session will open in the terminal, which can be closed by typing 'q'.

More complex usage would involve integrating valenchat into another chatbot. It is possible by initialising a bot and calling its questioning and memorising functions:

```
from datetime import datetime
from valencechat.bot import Chat
  
session_id = datetime.now().strftime('%Y-%m-%d-%H:%M')
questioner = Chat('de', session_id)

frame = Frame('Schlaf', belief_holder='Alice', individual=False)
questioner.add_frame(frame)
goal, q = questioner.get_question()
user_input = input(f"BOT >> {q}\nUSER >> ")
user_input = user_input.rstrip('\n')
questioner.memorise_answer(goal, user_input, verbose=True)
```
