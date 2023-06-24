# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 23:33:06 2023

@author: jucoe
"""

import genanki
import random
import os
import re
from zipfile import ZipFile
import json
import sqlite3

class AnkiCardGenerator:
    def __init__(self, deck_name, deck_filename=None):
        self.model_id = random.randrange(1 << 30, 1 << 31)
        self.deck_id = random.randrange(1 << 30, 1 << 31)

        self.model = genanki.Model(
            self.model_id,
            'Simple Model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
            ],
            templates=[
                {
                    'name': 'Question -> Question-Answer',
                    'qfmt': '{{Question}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                },
            ])

        self.deck = genanki.Deck(
            self.deck_id,
            deck_name)

        if deck_filename and os.path.exists(deck_filename):
            self.load_deck(deck_filename)

    def add_card(self, question, answer, tags=None):
        note = genanki.Note(
            model=self.model,
            fields=[question, answer],
            tags=tags)
        self.deck.add_note(note)

    def save_deck(self, filename='output.apkg'):
        genanki.Package(self.deck).write_to_file(filename)
        
    def load_deck(self, filename):
        with ZipFile(filename, 'r') as z:
            with z.open(r"C:\Users\jucoe\AppData\Roaming\Anki2\JucoenYeater\collection.anki2") as f:
                # Create an in-memory SQLite database
                con = sqlite3.connect(':memory:')
                cur = con.cursor()
                
                # Load the Anki SQLite database into memory
                cur.executescript(f.read().decode('utf-8'))
    
                # Query the notes table to get question, answer, and tags
                cur.execute("""
                    SELECT flds, tags
                    FROM notes
                """)
    
                for row in cur.fetchall():
                    fields = row[0].split('\x1f')
                    question = fields[0]
                    answer = fields[1]
                    tags = row[1].split()
    
                    # Replace spaces with underscores in tags
                    tags = [tag.replace(" ", "_") for tag in tags]
    
                    self.add_card(question, answer, tags=tags)
    
                con.close()

# =============================================================================
#     def load_deck(self, filename):
#         with ZipFile(filename, 'r') as z:
#             with z.open('collection.anki2') as f:
#                 data = json.load(f)
#                 for note in data['notes']:
#                     question = note['fields'][0]
#                     answer = note['fields'][1]
#                     tags = note['tags']
#                     self.add_card(question, answer, tags=tags)
# =============================================================================
                    

# =============================================================================
# def parse_question_answer_pairs(filename):
#     with open(filename, 'r') as f:
#         content = f.read()
# 
#     pattern = re.compile(r'(?:Q(?:uestion)?\d*[:.]?|Question \d*[:.]?)\s*(.+?)\s*(?:A(?:nswer)?\d*[:.]?|Answer \d*[:.]?)\s*(.+?)\s*Tags:\s*(.+?)(?=(?:Q(?:uestion)?\d*[:.]?|Question \d*[:.]?)|$)', re.DOTALL)
# 
#     question_answer_tags = [(match[0].strip(), match[1].strip(), [tag.replace(' ', '_') for tag in match[2].strip().split(', ')]) for match in pattern.findall(content)]
# 
#     return question_answer_tags
# 
# # Usage example:
# generator = AnkiCardGenerator(deck_name='Trivia Questions')
# filename = 'questions_answers.txt'  # Replace with the path to your text file containing questions, answers, and tags.
# 
# for question, answer, tags in parse_question_answer_pairs(filename):
#     generator.add_card(question, answer, tags=tags)
# 
# generator.save_deck('trivia_deck.apkg')
# =============================================================================


# =============================================================================
# # Usage example:
# generator = AnkiCardGenerator(deck_name='Country Capitals')
# generator.add_card('What is the capital of France?', 'Paris', tags=['geography', 'France'])
# generator.add_card('What is the capital of Italy?', 'Rome', tags=['geography', 'Italy'])
# generator.save_deck('example_deck.apkg')
# 
# # Loading an existing deck and adding a card
# loaded_generator = AnkiCardGenerator(deck_name='Country Capitals', deck_filename='example_deck.apkg')
# loaded_generator.add_card('What is the capital of Germany?', 'Berlin', tags=['geography', 'Germany'])
# loaded_generator.save_deck('updated_example_deck.apkg')
# =============================================================================
