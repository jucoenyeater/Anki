# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 00:10:19 2023

@author: jucoe
"""

class AnkiCardParser:
    global question_line, question
    def __init__(self, filename):
        self.filename = filename

    def clean_tags(self, tags):
        cleaned_tags = [tag.replace(' ', '_') for tag in tags.split(', ')]
        return cleaned_tags

    def process_match(self, match):
        question = match[0].strip()
        answer = match[1].strip()
        tags = self.clean_tags(match[2].strip())
        return question, answer, tags

    def parse_question_answer_pairs(self):
        global question, question_line
        question_answer_tags = []
    
        with open(self.filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 4):
                question_line = lines[i].strip()
# =============================================================================
#                 print(question_line)
# =============================================================================
                answer_line = lines[i + 1].strip()
# =============================================================================
#                 print(answer_line)
# =============================================================================
                tags_line = lines[i + 2].strip()
# =============================================================================
#                 print(tags_line)
# =============================================================================

                if (not question_line.startswith("Question:") and not question_line.startswith("Q:")) or (not answer_line.startswith("Answer:") and not answer_line.startswith("A:")) or not tags_line.startswith("Tags"):
                    continue
                
                if question_line.startswith("Question:"):
                    question = question_line[9:].strip()
                elif question_line.startswith("Q:"):
                    question = question_line[2:].strip()
                
                if answer_line.startswith("Answer:"):
                    answer = answer_line[7:].strip()
                elif answer_line.startswith("A:"):
                    answer = answer_line[2:].strip()
                
# =============================================================================
#                 for tag in tags_line[5:].strip().split(", "):
#                     print(tag.replace(" ", "_").lower())
# =============================================================================
                tags = [tag.replace(" ", "_").lower() for tag in tags_line[5:].strip().split(", ")]
                print(tags)

    
                question_answer_tags.append((question, answer, tags))
    
        return question_answer_tags