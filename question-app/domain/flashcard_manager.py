from typing import List

from sqlalchemy import String

class Flashcard:
    __tablename__ = "flashcards"
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def from_json(cls, json_data):
        return cls(json_data["question"], json_data.get("answer", ""))
    
class Deck:
    def __init__(self, name, summary="", flashcards=[]):
        self.name = name
        self.summary:str = summary
        self.flashcards:List[Flashcard] = flashcards
    def add_flashcard(self, flashcard:Flashcard):
        self.flashcards.append(flashcard)
    def get_flashcards(self):
        return self.flashcards
    def get_previous_questions(self):
        return [flashcard.question for flashcard in self.flashcards]
    
class FlashcardManager:
    def __init__(self):
        self.decks = {}
    def add_deck(self, deck:Deck):
        self.decks.update({deck.name: deck})
    def get_deck(self, name):
        return self.decks.get(name)
    def get_decks(self):
        return self.decks
    
