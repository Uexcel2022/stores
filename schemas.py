
from marshmallow import Schema, fields, validate


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainTag(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

# class PlainItemTag(Schema):
#     id = fields.Int(dump_only=True)
#     item_id = fields.Int(required=True)
#     tag_id = fields.Int(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True,load_only=True)
    store = fields.Nested(PlainItemSchema(),dump_only=True)
    tags = fields.List(fields.Nested(PlainTag()),dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    tags = fields.List(fields.Nested(PlainTag()),dump_only=True)

class TagSchema(PlainTag):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(StoreSchema(),dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema())
    Tags = fields.Nested(TagSchema())

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True, validate=validate.Length(min=6,max=16))

