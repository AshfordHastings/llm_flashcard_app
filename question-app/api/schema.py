from marshmallow import Schema, fields, post_load


class DeckSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    summary = fields.String()
