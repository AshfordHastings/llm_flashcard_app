import pytest, json

@pytest.mark.usefixtures('populate_flashcard_data')
def test_get_deck_list(client):
    deck_id = 1
    resp = client.get(f"/api/decks/{deck_id}/flashcards/", headers={})
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 200
    assert message == 'OK'
    assert error == None

    assert all("id" in item.keys() for item in value)
    assert all("question" in item.keys() for item in value)
    assert all("answer" in item.keys() for item in value)

@pytest.mark.usefixtures('populate_deck_data')
def test_create_flashcard_batch(client, test_flashcard_payload_kubernetes):
    deck_id = 1
    payload = test_flashcard_payload_kubernetes

    resp = client.post(f"/api/decks/{deck_id}/flashcards/", data=json.dumps(payload), content_type='application/json', headers={})
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 201
    assert message == 'Created'
    assert error == None

    assert all("id" in item.keys() for item in value)
    assert all("question" in item.keys() for item in value)
    assert all("answer" in item.keys() for item in value)
