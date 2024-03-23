import pytest

from flashcard_manager import Flashcard, Deck, FlashcardManager

def test_flashcard():
    flashcard = Flashcard("What is the capital of France?", "Paris")
    assert flashcard
    assert flashcard.question == "What is the capital of France?"
    assert flashcard.answer == "Paris"

    flashcard_json = {"question": "What is the capital of France?", "answer": "Paris"}
    flashcard_from_json = Flashcard.from_json(flashcard_json)
    assert flashcard_from_json
    assert flashcard_from_json.question == "What is the capital of France?"
    assert flashcard_from_json.answer == "Paris"
