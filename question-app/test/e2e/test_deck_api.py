import pytest

@pytest.mark.usefixtures('populate_deck_data')
def test_get_deck_list(client):
    resp = client.get(f"/decks/", headers={})
   
    message, value, error = resp.json.get('message', None), resp.json.get('value', None), resp.json.get('error', None)

    assert resp.status_code == 200
    assert message == 'OK'
    assert error == None

    assert all("id" in item.keys() for item in value)
    assert all("name" in item.keys() for item in value)
