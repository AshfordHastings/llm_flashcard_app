import pytest, json

@pytest.mark.usefixtures('populate_deck_data')
def test_get_deck_list(client):
    resp = client.get(f"/api/decks/", headers={})
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 200
    assert message == 'OK'
    assert error == None

    assert all("id" in item.keys() for item in value)
    assert all("name" in item.keys() for item in value)

@pytest.mark.usefixtures('populate_deck_data', 'populate_flashcard_data')
def test_get_deck_resource(client):
    deck_id = 1
    resp = client.get(f"/api/decks/{deck_id}", headers={})

    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 200
    assert message == 'OK'
    assert error == None

    assert "id" in value.keys()
    assert "name" in value.keys()
    assert "summary" in value.keys()
    #assert "flashcards" in value.keys()

def test_create_deck_resource(client):
    
    payload = {
        "name": "Test Deck 2",
        "summary": "This is a test deck."
    }

    resp = client.post(f"/api/decks/", data=json.dumps(payload), content_type='application/json', headers={})
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 201
    assert message == 'Created'
    assert error == None

    assert "id" in value.keys() 
    assert "name" in value.keys()
    assert "summary" in value.keys()

