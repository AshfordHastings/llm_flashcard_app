import json, traceback
from flask import Blueprint, request, jsonify, g

from api.schema import DeckSchema, FlashcardSchema
from api.responses import (
    response_with,
    SUCCESS_200,
    SUCCESS_201,
    SUCCESS_204,
    ERROR_500
)
from db import db_ops

flashcard_bp = Blueprint("flashcard_bp", __name__, url_prefix='/api/decks/<int:deck_id>/flashcards')

@flashcard_bp.route("/", methods=["GET"])
def get_flashcard_list(deck_id:int): 
    session = g.db_session

    try:
        schema = FlashcardSchema(many=True, exclude=['deckId'])

        obj_flashcard_list = db_ops.query_flashcard_list_by_deck_id(session, deck_id=deck_id)
        dict_flashcard_list = schema.dump(obj_flashcard_list)
    except Exception as e:
        traceback.print_exc()
        return response_with(ERROR_500, errors=(str(e)))
    return response_with(SUCCESS_200, value=dict_flashcard_list)

@flashcard_bp.route("/", methods=["POST"])
def create_flashcards(deck_id: int): 
    session = g.db_session
    schema = FlashcardSchema(many=True)

    data = request.json

    for flashcard in data:
        flashcard['deckId'] = deck_id

    try:
        obj_flashcard_list = schema.load(data)
        obj_flashcard_list_peristed = db_ops.insert_flashcard_batch(session, obj_flashcard_list)
        dict_flashcard_list_persisted = schema.dump(obj_flashcard_list_peristed)
    except Exception as e:
        traceback.print_exc()
        return response_with(ERROR_500, errors=(str(e)))

    return response_with(SUCCESS_201, value=dict_flashcard_list_persisted)