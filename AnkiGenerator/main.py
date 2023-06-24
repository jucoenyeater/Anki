# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 02:38:35 2023

@author: jucoe
"""

import argparse
from anki_connect import AnkiConnect, ConfigFileManager
from anki_card_parser import AnkiCardParser


def main(args=None):
    global question_answer_tags, default_settings_deck_config, cloned_config_id, updated_config, default_config, config_id, question, question_lines
    # Used if ran from the terminal
    if args is None:
        parser = argparse.ArgumentParser(description='Generate Anki cards from a text file with questions, answers, and tags.')
        parser.add_argument('input_file', help='Path to the input text file containing questions, answers, and tags.')
        parser.add_argument('--deck_name', default='Trivia Questions', help='Name of the Anki deck.')

        args = parser.parse_args()

    # Init the AnkiCardParser class
    anki_card_parser = AnkiCardParser(args.input_file)
    
    # Grab Question/Answer pairs to be loaded into Anki
    question_answer_tags = anki_card_parser.parse_question_answer_pairs()

    # Init the AnkiConnect class
    anki_connect = AnkiConnect()

    # Check if the deck exists
    deck_exists = anki_connect.deck_exists(args.deck_name)
    
    # Create the deck if it doesn't exist
    if not deck_exists:
        anki_connect.create_deck(args.deck_name)
    
    # Initialize the ConfigFileManager class
    config_manager = ConfigFileManager()
    
    # Load the config_ids from the JSON file
    config_ids = config_manager.load_config_ids()
    
    # Check if the config_id for args.deck_name exists
    config_id = config_ids.get(args.deck_name)
    
    # If the config_id doesn't exist, clone the "Default Settings" deck's config
    if config_id is None:

        default_config = anki_connect.get_deck_config("Default Settings")
        config_id = anki_connect.clone_deck_config(args.deck_name, default_config["id"])
        
        # Update new cards per day to 30
        updated_config = default_config.copy()
        updated_config["new"]["perDay"] = 30
        
        # Add the config to the JSON file
        config_manager.add_config_id(args.deck_name, config_id)
        # Save the updated configuration
        anki_connect.save_deck_config(updated_config) 
        # Set the config_id for the created deck
        anki_connect.set_deck_config(args.deck_name, config_id)

    # Add cards to the new deck
    for question, answer, tags in question_answer_tags:
        anki_connect.add_note(args.deck_name, "Basic", question, answer, tags=tags)



if __name__ == '__main__':
    class Args:
        input_file = 'questions_answers.txt'
        deck_name = "GPT3.5 Generated Pairs"

    main(args=Args())
