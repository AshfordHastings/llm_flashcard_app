import json,pytest

@pytest.mark.usefixtures('populate_flashcard_data')
def test_generate_questions_previous_songs(client):
    deck_id = "1"
    payload = {
        "specifications": "Generate questions focusing on Ingress and Service Discovery in Kubernetes.",
        "num_questions": 5
    }
    resp = client.post(f"/api/decks/{deck_id}/generate", data=json.dumps(payload), content_type='application/json', headers={})
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    print(resp)
    assert resp.status_code == 200
    assert message == 'OK'
    assert error == None

    print(f"Questions: {value}")

    assert type(value) == list
    assert len(value) == 5
    assert all(isinstance(item, dict) for item in value)
    assert all("question" in item for item in value)
    assert all("answer" in item for item in value)

    # assert all("id" in item.keys() for item in value)
    # assert all("name" in item.keys() for item in value)
