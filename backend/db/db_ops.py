from typing import List
from sqlalchemy.orm import Session
from exc import ResourceNotFound
from db.model import FlashcardModel, DeckModel

### DECKS ### 
def query_deck_list(session:Session) -> List[DeckModel]: 
    resp_deck_list = session.query(DeckModel).all()
    return resp_deck_list

def query_deck_resource(session:Session, deck_id:int) -> DeckModel:
    resp_deck_resource = session.query(DeckModel).filter_by(id=deck_id).first()
    if resp_deck_resource is None:
        raise ResourceNotFound(f"Deck resource with id of {deck_id} is not found.")
    return resp_deck_resource

def insert_deck_resource(session:Session, data:DeckModel) -> DeckModel: 
    session.add(data)
    session.flush()
    return data

def update_deck(session:Session, deck_id:int, deck_data:dict ) -> DeckModel:
    existing_deck = session.query(DeckModel).filter_by(id=deck_id).first()
    if not existing_deck:
        raise ResourceNotFound(f"Deck resource with id of {deck_id} is not found.")
    for key, value in deck_data.items():
        setattr(existing_deck, key, value)
    
    session.flush()
    return existing_deck

def delete_deck_resource(session:Session, deck_id:int):
    resp_deck_resource = session.query(DeckModel).filter_by(id=deck_id).first()
    if resp_deck_resource:
        session.delete(resp_deck_resource)
        session.flush()
    else:
        raise ResourceNotFound(f"Deck resource with id of {deck_id} is not found.")


### FLASHCARDS ###
# def query_flashcard_list_by_deck_id(session:Session, deck_id:int) -> List[FlashcardModel]: 
#     resp_flashcard_list = session.query(FlashcardModel).\
#         join(FlashcardOrderModel, FlashcardModel.id == FlashcardOrderModel.flashcard_id).\
#         filter(FlashcardModel.deck_id == deck_id).\
#         order_by(FlashcardOrderModel.position.asc()).\
#         all()

#     return resp_flashcard_list

def query_flashcard_list_by_deck_id(session:Session, deck_id:int) -> List[FlashcardModel]: 
    resp_flashcard_list = session.query(FlashcardModel).\
        filter(FlashcardModel.deck_id == deck_id).\
        all()
    return resp_flashcard_list

def insert_flashcard_batch(session:Session, data:List[FlashcardModel]) -> List[FlashcardModel]: 
    session.add_all(data)
    session.flush()
    return data

def update_flashcard(session:Session, flashcard_id:int, flashcard_data:dict ) -> FlashcardModel:
    existing_flashcard = session.query(FlashcardModel).filter_by(id=flashcard_id).first()
    if not existing_flashcard:
        raise ResourceNotFound(f"Flashcard resource with id of {flashcard_id} is not found.")
    for key, value in flashcard_data.items():
        setattr(existing_flashcard, key, value)
    
    session.flush()
    return existing_flashcard

def delete_flashcard(session:Session, flashcard_id:int):
    existing_flashcard = session.query(FlashcardModel).filter_by(id=flashcard_id).first()
    if not existing_flashcard:
        raise ResourceNotFound(f"Flashcard resource with id of {flashcard_id} is not found.")
    session.delete(existing_flashcard)
    session.flush()

# def calculate_new_position(session:Session, flashcard_id:int, target_position:int):
    