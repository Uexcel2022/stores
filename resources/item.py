import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import  items
from schemas import ItemSchema,ItemUpdateSchema

blp = (
    Blueprint('item', __name__, description='Item related operations'))

@blp.route('/stores/items')
class Item(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()


    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self,posted_item):

        for _, item in items.items():
            if (posted_item.get('store_id') == item.get('store_id')
                    and posted_item.get('name') == item.get('name')):
                abort(http_status_code=409, message="The item already exists.")

        item_id = uuid.uuid4().hex
        items[item_id] = {**posted_item, "id": item_id}
        return items[item_id]


@blp.route('/stores/<string:item_id>/items')
class ItemList(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = items.get(item_id)
        if not item:
            abort(http_status_code=404, message="The item not found")
        return item

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, posted_item, item_id):
        if not item_id:
            abort(http_status_code=400, message="Please provide item id")

        if not items.get(item_id):
            abort(http_status_code=404, message="the item not found")

        item = items[item_id]
        item |= posted_item

        return items[item_id]

    @blp.response(204)
    def delete(self, item_id):
        if not item_id:
            abort(http_status_code=400, message="Please provide item id")

        if not items.get(item_id):
            abort(http_status_code=404, message="The item not found")

        print(items.pop(item_id))

        return {"message":"The item deleted successfully"}
