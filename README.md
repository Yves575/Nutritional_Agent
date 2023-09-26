# Rasa Chatbot Project
This project is a Rasa-based chatbot that collects user preferences and provides personalized recommendations. The chatbot is equipped with various functionalities like handling user interactions, validating form inputs, and more.

## Table of Contents
1. Install Dependencies
1. Files Description
1. Usage
1. Dependencies


## Install Dependencies
```
pip install -r requirements.txt
```

## Files Description
* NLU and Training Data:

Defines intents, entities, lookup tables, and training examples for Rasa's Natural Language Understanding.
* Rules and Stories:

Contains the rules and stories which guide the conversation flow of the chatbot.
* Actions:

Implements custom actions used in the conversation, such as validating form inputs and storing user data.
* User Interaction Script:

A script to interact with Furhat
## Usage
**The commands must be used in the root of your Rasa project**
1. **Train the Rasa Model:**
```
rasa train
```
*Be carful if you train a new model you should also change it in the furhat_agent.py program.* 

*Note that a model is already present in the project system.*

2. **Enabling the HTTP API**
```
rasa run --enable-api
```
**WARNING: you might have to re-execute this command if the virtual agent doesn't reply anymore. It mostly occure when you execute for a second time the main program (furhat_agent.py).**

*Open another terminal and activate the virtual environment to proceed to the next step.*

3. **Run the Rasa Actions Server:**
```
rasa run actions
```
*Open another terminal and activate the virtual environment to proceed to the next step.*

4. **Interact with the Chatbot:**

Run the user interaction script:
```
python furhat_agent.py
```

## Dependencies
To see a list of dependencies used in this project, refer to the requirements.txt file:
```
cat requirements.txt
```