import json,pytest

def test_generate_questions_previous_songs(client):
    payload = {
        # "specifications": "Generate questions focusing on Ingress and Service Discovery in Kubernetes.",
        "question": "What is Ingress in Kubernetes?",
    }
    resp = client.post(f"/api/llm/generate-answer", data=json.dumps(payload), content_type='application/json', headers={})
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    print(error)
    assert resp.status_code == 200
    assert message == 'OK'
    assert error == None

    print(f"Answer: {value}")

    assert type(value) == dict
    assert "answer" in value