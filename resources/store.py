import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import  stores
from schemas import StoreSchema

blp = (
    Blueprint('store', __name__, description='Store related operations'))

@blp.route('/stores')
class Store(MethodView):
    def get(self):
        return {"stores": list(stores.values())}
    @blp.arguments(StoreSchema)
    def post(self, store_data):
        store_id = uuid.uuid4().hex

        for _, store in stores.items():
            if store.get("name") == store_data.get("name"):
                abort(409, message="The store already exists")

        new_store = {"store_id": store_id, **store_data}
        stores[store_id] = new_store
        return stores[store_id], 201


@blp.route('/stores/<string:store_id>')
class StoreList(MethodView):
    def get(self,store_id):
        store_data = stores.get(store_id)
        if not store_data:
            abort(404, message="The store not found.")
        return store_data, 200

    @blp.arguments(StoreSchema)
    def put(self,store_data, store_id):

        if not stores.get(store_id):
            abort(http_status_code=404, message="The store not found")

        stores[store_id]['name'] = store_data["name"]

        return {'item': stores[store_id]}, 200


    def delete(self,store_id):
        if not store_id:
            abort(http_status_code=400, message="Please provide store id")

        if not stores.get(store_id):
            abort(http_status_code=404, message="The store not found")

        stores.pop(store_id)

        return {'message': 'store delete!'}, 204