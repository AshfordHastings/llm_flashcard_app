from marshmallow import Schema, fields, post_load

from db.model import DeckModel, FlashcardModel

class FlashcardSchema(Schema): 
    id = fields.Integer(dump_only=True)
    question = fields.String(default="")
    answer = fields.String(default="")

    deck_id = fields.Integer()

    @post_load
    def make_flashcard(self, data, **kwargs):
        return FlashcardModel(**data)

    # @post_load(pass_many=)

class DeckSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    summary = fields.String()

    #flashcards = fields.Nested(FlashcardSchema, many=True, exclude=("deckId",))

    @post_load
    def make_deck(self, data, **kwargs):
        return DeckModel(**data)
    
