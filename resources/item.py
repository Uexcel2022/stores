import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import  items,stores
from schemas import ItemSchema,ItemUpdateSchema

blp = (
    Blueprint('item', __name__, description='Item related operations'))

@blp.route('/stores/items')
class Item(MethodView):
    def get(self):
        return {'items': list(items.values())}, 200
    @blp.arguments(ItemSchema)
    def post(self,posted_item):
        # posted_item = request.get_json()
        # if not posted_item.get("store_id") or not posted_item.get("name") or not posted_item.get("price"):
        #     abort(http_status_code=400, message="One or more properties are missing.")
        #
        # if not stores.get(posted_item.get("store_id")):
        #     abort(http_status_code=404, message="The store not found.")

        for _, item in items.items():
            if (posted_item.get('store_id') == item.get('store_id')
                    and posted_item.get('name') == item.get('name')):
                abort(http_status_code=409, message="The item already exists.")

        item_id = uuid.uuid4().hex
        items[item_id] = {**posted_item, "item_id": item_id}
        return {"item": items[item_id]}, 201


@blp.route('/stores/<string:item_id>/items')
class ItemList(MethodView):
    def get(self, item_id):
        item_data = items.get(item_id)
        if not item_data:
            abort(http_status_code=404, message="The item not found")
        return {'item': item_data}, 200

    @blp.arguments(ItemUpdateSchema)
    def put(self, posted_item, item_id):
        if not item_id:
            abort(http_status_code=400, message="Please provide item id")

        if not items.get(item_id):
            abort(http_status_code=404, message="the item not found")

        item = items[item_id]
        item |= posted_item

        return {'item': items[item_id]}, 200


    def delete(self, item_id):
        if not item_id:
            abort(http_status_code=400, message="Please provide item id")

        if not items.get(item_id):
            abort(http_status_code=404, message="The item not found")

        print(items.pop(item_id))

        return {'message': 'Item delete!'}, 204
