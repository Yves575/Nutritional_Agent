# Necessary imports for the custom actions
from typing import Text, List, Any, Dict
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import pandas as pd
import random
from rasa_sdk.events import BotUttered
from rasa_sdk.events import SlotSet
import csv

# This class defines the custom action for summarizing the collected data from the user.
class ActionSayData(Action):
    def name(self) -> Text:
        return "action_say_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response_text = "Here's the data you requested."

        # Extracting the slot values from the conversation.
        age = tracker.get_slot("age")
        gender = tracker.get_slot("gender")
        weight = tracker.get_slot("weight")
        height = tracker.get_slot("height")
        sport = tracker.get_slot("sport")
        mealtype = tracker.get_slot("mealtype")
        allergen = tracker.get_slot("allergen")
        habits = tracker.get_slot("habits")
        disliked = tracker.get_slot("disliked")
        
        # Sending a response to the user summarizing the collected data.
        # ONLY executed when all the slots are fulfilled 
        dispatcher.utter_message(text=f"Great! We have all the information, You are {age} year old, you are also {gender} and you dislike {disliked}. Or {habits}")
        dispatcher.utter_message(text=f"Some other information about yourself: Your are {weight}kg and {height}cm, you do {sport} activity. Here {mealtype} but {allergen}")
        
        # Create the CSV file
        csv_file_name = 'result_data.csv'
        header = ['age', 'gender', 'weight', 'height', 'sport', 'mealtype', 'allergen', 'habits', 'disliked']
        data = [age, gender, weight, height, sport, mealtype, allergen, habits, disliked]

        # Write to the CSV file
        with open(csv_file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(data)

        return [BotUttered(text=response_text)]

# Sending a response to the user summarizing the collected data.
class ValidateSimpleForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_simple_form"    

    # Utility function to fetch unique values for features from a CSV file.
    @staticmethod
    def feature_db(feature: str) -> List[Text]:
        df = pd.read_csv('data/UserDatFRS.csv')
        distinct_df = df[feature].str.lower().unique().tolist()
        return distinct_df

    # Validation functions for each slot in the form.
    def validate_height(self, slot_value: Any, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        height = tracker.get_slot("height")
        height = height.replace(",", "").replace(".","")

        if(len(height) != 3):
            dispatcher.utter_message(text="Invalid height, please input correctly your height")
            return{"height":None}
        else:
            return{"height":height}

    def validate_gender(self, slot_value: Any, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        gender = tracker.get_slot("gender")

        if gender.lower() in self.feature_db("gender"):
            return {"gender": gender}
        else:
            dispatcher.utter_message(text=f"I'm sorry but this gender is not taken into account.\nHere the list of possibilities: {', '.join(self.feature_db('gender'))}")

            return {"gender": None}

    def validate_sport(self, slot_value: Any, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sport = tracker.get_slot("sport")

        if sport.lower() in self.feature_db("sports"):
            return {"sport": sport}
        else:
            dispatcher.utter_message(text=f"I'm sorry but this type of activity is not taken into account.\nHere the list of possibilities: {', '.join(self.feature_db('sports'))}")
            return {"sport": None}

    def validate_mealtype(self, slot_value: Any, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mealtype = tracker.get_slot("mealtype")

        if mealtype.lower() in self.feature_db("mealtype"):
            return {"mealtype": mealtype}
        else:
            dispatcher.utter_message(text=f"I'm sorry but this type of meal is not taken into account.\nHere the list of possibilities: {', '.join(self.feature_db('mealtype'))}")
            return {"mealtype": None}

    def validate_allergen(self, slot_value: Any, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        allergen = tracker.get_slot("allergen")

        if allergen.lower() in self.feature_db("allergies"):
            return {"allergen": allergen}
        else:
            dispatcher.utter_message(text=f"I'm sorry but this type of allergen is not taken into account.\nHere the list of possibilities: {', '.join(self.feature_db('allergies'))}")
            return {"allergen": None}

    def validate_habits(self, slot_value: Any, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        habits = tracker.get_slot("habits")

        if habits.lower() in self.feature_db("habits"):
            return {"habits": habits}
        else:
            dispatcher.utter_message(text=f"I'm sorry but this type of habits is not taken into account.\nHere the list of possibilities: {', '.join(self.feature_db('habits'))}")
            return {"habits": None}

    def validate_disliked(self, slot_value: Any, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        disliked = tracker.get_slot("disliked")

        if disliked.lower() in self.feature_db("disliked_ingredients"):
            return {"disliked": disliked}
        else:
            dispatcher.utter_message(text=f"I'm sorry but this type of food is not taken into account.\nHere the list of some possibilities: {', '.join((self.feature_db('disliked_ingredients'))[:5])}")
            return {"disliked": None}

# This class defines an action to skip a step in the conversation.
class ActionSkip(Action):
    def name(self) -> str:
        return "action_skip"

    async def run(
        self, dispatcher, tracker, domain: DomainDict
    ) -> list:
        # Get the name of the currently requested slot
        requested_slot = tracker.get_slot("requested_slot")

        # If there is a requested slot, skip it by setting it to None
        if requested_slot:
            return [SlotSet(requested_slot, "None")]

        # Otherwise, continue normally
        return []

    
