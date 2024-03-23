import json, traceback
from flask import Blueprint, request, jsonify, g

from api.schema import DeckSchema
from api.responses import (
    response_with,
    SUCCESS_200,
    SUCCESS_201,
    SUCCESS_204,
    ERROR_500
)
from db import db_ops
from llm_interface import LLMInterface

deck_bp = Blueprint("deck_bp", __name__) 

@deck_bp.route("/", methods=["GET"])
def get_deck_list():
    session = g.db_session
    schema = DeckSchema(many=True)

    obj_deck_list = db_ops.query_deck_list(session)
    dict_deck_list = schema.dump(obj_deck_list)

    return response_with(SUCCESS_200, value=dict_deck_list)

@deck_bp.route('/<deck_id>', methods=["GET"])
def get_deck_resource(deck_id):
    session = g.db_session
    schema = DeckSchema()

    obj_deck_resource = db_ops.query_deck_resource(session, deck_id)
    dict_deck_resource = schema.dump(obj_deck_resource)

    return response_with(SUCCESS_200, dict_deck_resource)

@deck_bp.route('/', methods=["POST"])
def create_deck_resource():
    session = g.db_session
    schema = DeckSchema()
    try:
        data = request.json
        obj_deck_resource = schema.load(data)
        obj_deck_resource_persisted = db_ops.insert_deck_resource(session, obj_deck_resource)
        dict_deck_resource_persisted = schema.dump(obj_deck_resource_persisted)
    except Exception as e:
        print(e)
        return response_with(ERROR_500, errors=e)


    return response_with(SUCCESS_201, dict_deck_resource_persisted)

@deck_bp.route('/<deck_id>', methods=["DELETE"])
def remove_deck_resource(deck_id):
    session = g.db_session

    try:
        db_ops.delete_deck_resource(session, deck_id)
    except Exception as e:
        print(e)
        pass

    return response_with(SUCCESS_204)


@deck_bp.route('/<deck_id>/generate', methods=["POST"])
def generate_questions(deck_id):
    session = g.db_session
    schema = DeckSchema()
    llm_interface = LLMInterface()

    try:
        obj_deck_resource = db_ops.query_deck_resource(session, deck_id)
        #dict_deck_resource = schema.dump(obj_deck_resource)
        data = request.json
        specifications = data.get("specifications", "")
        num_questions = data.get("num_questions", 1)
    
        deck = obj_deck_resource.convert_to_domain()
        questions = llm_interface.generate_questions_for_deck(deck, specifications, num_questions)
    except Exception as e: 
        traceback.print_exc()
        return response_with(ERROR_500, errors=str(e))



    return response_with(SUCCESS_200, value=questions)


