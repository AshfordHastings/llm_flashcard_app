import json, traceback
from flask import Blueprint, request, jsonify, g

from api.responses import (
    response_with,
    SUCCESS_200,
    SUCCESS_201,
    SUCCESS_204,
    BAD_REQUEST_400,
    ERROR_500
)
from llm import LLMQuestionCreator, LLMAnswerer
llm_bp = Blueprint("llm_bp", __name__, url_prefix='/api/llm')

@llm_bp.route("/answers/generate", methods=["POST"])
def generate_answer():
    data = request.json
    question = data.get("question", "")

    if not question:
        return response_with(BAD_REQUEST_400, errors="Question is required.")
    
    try:
        llm = LLMAnswerer()
        response = llm.generate_answer(question)
    except Exception as e:
        traceback.print_exc()
        return response_with(ERROR_500, errors=(str(e)))
    
    return response_with(SUCCESS_200, value=response)
    
@llm_bp.route("/questions/generate", methods=["POST"])
def generate_qa():
    data = request.json
    specifications = data.get("specifications", "")
    num_questions = data.get("num_questions", 1)
    previous_questions = data.get("previous_questions", [])

    if not specifications:
        return response_with(BAD_REQUEST_400, errors="Specifications are required.")
    
    try:
        llm = LLMQuestionCreator()
        response = llm.generate_questions(specifications, num_questions, previous_questions=previous_questions)
    except Exception as e:
        traceback.print_exc()
        return response_with(ERROR_500, errors=(str(e)))
    
    return response_with(SUCCESS_200, value=response)
    

