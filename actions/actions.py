# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_when_open"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        print(entities)
        print("-------------------")
        print(entities[0]['value'])
        hours = []
        days = []
        now = datetime.now()
        current_hour = now.hour
        current_day = now.strftime("%A")
        for item in entities:
            if item['entity'] == 'hour':
                hours.append(item['value'])
            elif item['entity'] == 'day':
                days.append(item['value'])
        
        if hours and hours[0] == 'now':
            hours[0] = (str(current_hour))
            if not days:
                days.append((str(current_day)))
            days[0] = (str(current_day))
        hour_values = [hour[:2] for hour in hours if len(hour) >= 2]
        
        if any(8 <= int(hour) <= 22 for hour in hour_values) and days != "Sunday":
            var = "Yes, the restaurant is open: " + ', '.join(hours) + " " + ', '.join(days)
            dispatcher.utter_message(text=var)
        else:
            var = "No, the restaurant is not open: " + ', '.join(hours) + " " + ', '.join(days)
            dispatcher.utter_message(text=var)
        return []

class ActionMenu(Action):

    def name(self) -> Text:
        return "action_order_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        print(entities)
        print("-------------------")
        if not entities or not entities[0].get('value'):
            var = "We don't have that dish on the menu :)"
            dispatcher.utter_message(text=var)
            return []
        print(entities[0]['value'])
        food = []
        without = []

        for item in entities:
            if item['entity'] == 'food_item':
                food.append(item['value'])
            elif item['entity'] == 'topping':
                without.append(item['value'])
        if not without:
            var = "Your dish has been added to the order. Do you want something more?"
        else:
            var = "Your application has been added to your order according to your preferences. Do you want something more?"
        dispatcher.utter_message(text=var)
        return []

class ActionFinish(Action):

    def name(self) -> Text:
        return "action_finish"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        var = "Thanks. The order will be ready after 20 minutes :)"
        dispatcher.utter_message(text=var)
        return []