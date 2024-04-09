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
from llm.llm_answers import QuestionAnswerer
from llm.llm_qa import LLMQA

llm_bp = Blueprint("llm_bp", __name__, url_prefix='/api/llm')

@llm_bp.route("/generate-answer", methods=["POST"])
def generate_answer():
    data = request.json
    question = data.get("question", "")
    specifications = data.get("specifications", "")

    if not question:
        return response_with(BAD_REQUEST_400, errors="Question is required.")
    
    try:
        llm = QuestionAnswerer()
        response = llm.generate_answer(question, specifications)
    except Exception as e:
        traceback.print_exc()
        return response_with(ERROR_500, errors=(str(e)))
    
    return response_with(SUCCESS_200, value=response)
    
@llm_bp.route("/generate-qa", methods=["POST"])
def generate_qa():
    data = request.json
    instructions = data.get("instructions", "")
    questions_count = data.get("question_count", 1)

    if not instructions:
        return response_with(BAD_REQUEST_400, errors="Instructions are required.")
    
    try:
        llm = LLMQA()
        response = llm.generate_questions(instructions, questions_count)
    except Exception as e:
        traceback.print_exc()
        return response_with(ERROR_500, errors=(str(e)))
    
    return response_with(SUCCESS_200, value=response)
    

