import json 
import pytest

from llm_interface import LLMInterface


def test_generate_questions():
    llm_interface = LLMInterface()
    deck_summary = "Flashcards to Learn About the Kubernetes"
    specifications = "Generate questions focusing on Ingress and Service Discovery in Kubernetes."

    response = llm_interface.generate_questions(deck_summary, specifications, num_questions=5)

    assert response
    print(response)
    #dict_response = json.loads(response)
    assert response
    assert isinstance(response, list)
    assert len(response) == 5
    assert all(isinstance(item, dict) for item in response)
    assert all("question" in item for item in response)
    assert all("answer" in item for item in response)

