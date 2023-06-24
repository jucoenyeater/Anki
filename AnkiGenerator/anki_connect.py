# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 02:15:40 2023

@author: jucoe
"""

import requests
import json
import os
from typing import Dict, Optional

class ConfigFileManager:
    def __init__(self, config_file: str = "config_ids.json"):
        self.config_file = config_file
        if not os.path.exists(config_file):
            with open(config_file, "w") as f:
                json.dump({}, f)

    def load_config_ids(self) -> Dict[str, int]:
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        else:
            return {}

    def save_config_ids(self, config_ids: Dict[str, int]) -> None:
        with open(self.config_file, "w") as f:
            json.dump(config_ids, f)

    def add_config_id(self, config_name: str, config_id: int) -> None:
        config_ids = self.load_config_ids()
        config_ids[config_name] = config_id
        self.save_config_ids(config_ids)

    def remove_config_id(self, config_name: str) -> None:
        config_ids = self.load_config_ids()
        if config_name in config_ids:
            del config_ids[config_name]
            self.save_config_ids(config_ids)

    def get_config_id(self, config_name: str) -> Optional[int]:
        config_ids = self.load_config_ids()
        return config_ids.get(config_name)
    

class AnkiConnect:
    def __init__(self, host="http://127.0.0.1", port=8765):
        self.url = f"{host}:{port}/"

    def _invoke(self, action, params=None):
        request_data = {"action": action, "version": 6}
        if params:
            request_data["params"] = params
        response = requests.post(self.url, json=request_data).json()
        if len(response) > 0 and response.get("error") is None:
            return response["result"]
        else:
            raise Exception(f"Error with action {action}: {response.get('error')}")


    def create_deck(self, deck_name):
        return self._invoke("createDeck", {"deck": deck_name})
    
    def deck_exists(self, deck_name):
        decks = self._invoke('deckNames')
        return deck_name in decks


    def delete_deck(self, deck_name):
        return self._invoke("deleteDecks", {"decks": [deck_name]})

    def add_note(self, deck_name, model_name, question, answer, tags=None):
        if not tags:
            tags = []
            
        # Check if the note with the same question and answer already exists
        duplicate_note_ids = self._invoke("findNotes", {"query": f'deck:"{deck_name}" Front:"{question}" Back:"{answer}"'})
    
        if duplicate_note_ids:
            print(f"Skipping duplicate note: '{question}'")
            return
            
        note_data = {
            "modelName": model_name,
            "fields": {"Front": question, "Back": answer},
            "tags": tags,
            "options": {"allowDuplicate": False},
            "deckName": deck_name,
        }
        return self._invoke("addNote", {"note": note_data})

# =============================================================================
#     def update_note_fields(self, note_id, question=None, answer=None):
#         fields = {}
#         if question:
#             fields["Front"] = question
#         if answer:
#             fields["Back"] = answer
#         return self._invoke("updateNoteFields", {"note": {"id": note_id, "fields": fields}})
# 
#     def get_deck_info(self, deck_name):
#         return self._invoke("deckInfo", {"deck": deck_name})
# 
#     def get_notes(self, deck_name):
#         return self._invoke("findNotes", {"query": f'deck:"{deck_name}"'})
# 
#     def get_note_info(self, note_id):
#         return self._invoke("notesInfo", {"notes": [note_id]})
# =============================================================================
    
    def get_deck_config(self, deck_name):
        return self._invoke("getDeckConfig", {"deck": deck_name})
    
    def save_deck_config(self, config):
        return self._invoke("saveDeckConfig", {"config": config})

    def create_deck_config(self, config_name, config_data):
        return self._invoke("createDeckConfiguration", {"name": config_name, "config": config_data})
                                          
    def update_deck_config(self, config_id, config_data):
        config = self.get_deck_config_by_id(config_id)
        config.update(config_data)
        return self.save_deck_config(config)
    
    def set_deck_config(self, deck_name, config_id):
        return self._invoke("setDeckConfigId", {"decks": [deck_name], "configId": config_id})
   
    def clone_deck_config(self, new_config_name, source_config_id):
        return self._invoke("cloneDeckConfigId", {"name": new_config_name, "cloneFrom": source_config_id})