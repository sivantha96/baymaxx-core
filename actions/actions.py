import pymongo

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction


class CheckExistingUser(Action):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["baymaxx"]

    def name(self) -> Text:
        return "action_existing_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.current_state()['sender_id']
        col = self.db["users"]
        user = col.find_one({"user_id": user_id})
        return [{
            "event": "slot",
            "name": "is_existing_user",
            "value": "false"
        }]


class SaveUser(Action):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["baymaxx"]

    def name(self) -> Text:
        return "action_save_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.current_state()['sender_id']
        user_name = tracker.get_slot('name')
        user_age = tracker.get_slot('age')
        user_gender = tracker.get_slot('gender')
        col = self.db["users"]
        user = {"user_id": user_id, "name": user_name, "age": user_age, "gender": user_gender}
        col.insert_one(user)
        return [{
            "event": "slot",
            "name": "is_existing_user",
            "value": "true"
        }]
