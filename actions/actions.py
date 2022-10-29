from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import BotUttered
from calendar import calendar, calendar_api

class CreateTodo(Action):
    def name(self) -> Text:
        return "action_create_todo"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        todo = tracker.get_slot("todo")
        todo_list = tracker.get_slot("todo_list")
        todo_list.append(todo)
        print(todo_list)
        dispatcher.utter_message(response="utter_todo_added", todo=todo)
        return [SlotSet("todo", None), SlotSet("todo_list", todo_list)]
    
class ListTodo(Action):
    def name(self) -> Text:
        return "action_list_todo"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        todo_list = tracker.get_slot("todo_list")
        print(todo_list)
        todo_list = "".join([f"\n {idx+1}. {todo}" for idx,todo in enumerate(todo_list)])
        dispatcher.utter_message(response="utter_list_todo", todo_list=todo_list)
        return []
    
class CompleteTodo(Action):
    def name(self) -> Text:
        return "action_complete_todo"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        todo_number = tracker.get_slot("todo_number")
        todo_list = tracker.get_slot("todo_list")
        del todo_list[todo_number-1]
        print(todo_list)
        todo_list = "".join([f"\n {idx+1}. {todo}" for idx,todo in enumerate(todo_list)])
        dispatcher.utter_message(response="utter_list_todo", todo_list=todo_list)
        return [SlotSet("todo_number", None), SlotSet("todo_list", todo_list)]
    
class CreateEvent(Action):
    def name(self) -> Text:
        return "action_create_event"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        event = tracker.get_slot("event")
        date_time = tracker.get_slot("event_datetime")
        event = {}
        event["summary"] = event
        event["start"] = {"dateTime": date_time}
        calendar_api.create_event(event)
        dispatcher.utter_message(response="utter_event_added", event=event, date_time=date_time)
        return [SlotSet("event", None), SlotSet("event_datetime", None)]
    
class ListEvent(Action):
    def name(self) -> Text:
        return "action_list_event"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        events = calendar_api.list_recent_events()
        dispatcher.utter_message(response="utter_list_event")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            dispatcher.utter_message(response="utter_list_event", event=event['summary'], date_time=start)
        return []