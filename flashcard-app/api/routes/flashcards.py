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
        schema = FlashcardSchema(many=True, exclude=['deck_id'])

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
        flashcard['deck_id'] = deck_id

    print(f"REQUEST DATA: {data}")

    try:
        obj_flashcard_list = schema.load(data)
        obj_flashcard_list_peristed = db_ops.insert_flashcard_batch(session, obj_flashcard_list)
        session.commit() # Commit after successful batch insert

        dict_flashcard_list_persisted = schema.dump(obj_flashcard_list_peristed)
    except Exception as e:
        traceback.print_exc()
        return response_with(ERROR_500, errors=(str(e)))

    return response_with(SUCCESS_201, value=dict_flashcard_list_persisted)

@flashcard_bp.route("/<flashcard_id>", methods=["PUT"])
def modify_flashcard(deck_id:int, flashcard_id:int):
    session = g.db_session
    schema = FlashcardSchema()

    data = request.json

    # data['id'] = flashcard_id
    # data['deck_id'] = deck_id

    try:
        updated_flashcard = db_ops.update_flashcard(session, flashcard_id, data)
        session.commit()

        dict_updated_flashcard = schema.dump(updated_flashcard)
    except Exception as e:
        return response_with(ERROR_500, errors=(str(e)))
        #obj_flashcard = schema.load(data)
    
    return response_with(SUCCESS_201, value=dict_updated_flashcard)


@flashcard_bp.route("/<flashcard_id>", methods=["DELETE"])
def delete_flashcard(deck_id:int, flashcard_id:int):
    session = g.db_session

    try:
        db_ops.delete_flashcard(session, flashcard_id)
        session.commit()
    except Exception as e:
        return response_with(ERROR_500, errors=(str(e)))

    return response_with(SUCCESS_204)


# @flashcard_bp.route("/<flashcard_id>/generate-answer", methods=["POST"])
# def generate_answer(deck_id:int, flashcard_id:int):
#     session = g.db_session

#     try:
#         db_ops.delete_flashcard(session, flashcard_id)
#         session.commit()
#     except Exception as e:
#         return response_with(ERROR_500, errors=(str(e)))

#     return response_with(SUCCESS_204)



    
