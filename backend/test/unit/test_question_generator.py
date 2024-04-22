import json 
import pytest

from llm_interface import LLMInterface

@pytest.mark.skip()
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

@pytest.mark.skip()
def test_generate_questions_taylor_swift():
    llm_interface = LLMInterface()
    deck_summary = "Flashcards to Learn About Taylor Swift's Life"
    specifications = "I would like the questions to be pretty challenging and obscure. Only for dedicated fans. The questions should focus on her music."

    response = llm_interface.generate_questions(deck_summary, specifications, num_questions=5)

    assert response
    print(json.dumps(response, indent=2))
    #dict_response = json.loads(response)
    assert response
    assert isinstance(response, list)
    assert len(response) == 5
    assert all(isinstance(item, dict) for item in response)
    assert all("question" in item for item in response)
    assert all("answer" in item for item in response)


def test_generate_questions_repeat_questions():
    llm_interface = LLMInterface()
    deck_summary = "Flashcards to Learn About Kubernetes"
    specifications = "Generate questions focusing on Ingress and Service Discovery in Kubernetes."
    previous_questions = [
        "What is the primary function of Ingress in Kubernetes?",
        "How does Service Discovery work in Kubernetes?",
        "What is the main difference between NodePort and LoadBalancer service types in Kubernetes?",
        "Can you use Ingress without a service in Kubernetes?",
        "What is a Service in Kubernetes and what is it used for?"
    ]

    response = llm_interface.generate_questions(deck_summary, specifications, previous_questions, num_questions=5)

    assert response
    print(json.dumps(response, indent=2))
    #dict_response = json.loads(response)
    assert response
    assert isinstance(response, list)
    assert len(response) == 5
    assert all(isinstance(item, dict) for item in response)
    assert all("question" in item for item in response)
    assert all("answer" in item for item in response)
    assert all(item["question"] not in previous_questions for item in response)