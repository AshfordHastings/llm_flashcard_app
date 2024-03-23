from typing import List

from exc import ResourceNotFound
from db.model import FlashcardModel, DeckModel

### DECKS ### 
def query_deck_list(session) -> List[DeckModel]: 
    resp_deck_list = session.query(DeckModel).all()
    return resp_deck_list

def query_deck_resource(session, deck_id) -> DeckModel:
    resp_deck_resource = session.query(DeckModel).filter_by(id=deck_id).first()
    if resp_deck_resource is None:
        raise ResourceNotFound(f"Deck resource with id of {deck_id} is not found.")
    return resp_deck_resource

def insert_deck_resource(session, data): 
    session.add(data)
    session.flush()
    return data

def delete_deck_resource(session, deck_id):
    resp_deck_resource = session.query(DeckModel).filter_by(id=deck_id).first()
    if resp_deck_resource:
        session.delete(resp_deck_resource)
        session.flush()
    else:
        raise ResourceNotFound(f"Deck resource with id of {deck_id} is not found.")

