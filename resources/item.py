
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db

from models import ItemModel
from schemas import ItemSchema,ItemUpdateSchema

blp = (
    Blueprint('item', __name__, description='Item related operations'))

@blp.route('/stores/items')
class Item(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self,posted_item):
       item = ItemModel(**posted_item)
       try:
           db.session.add(item)
           db.session.commit()
           return item
       except SQLAlchemyError as e:
            abort(http_status_code=500,message="An error occurred!")

@blp.route('/stores/<int:item_id>/items')
class ItemList(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
            return ItemModel.query.get_or_404(item_id)


    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, posted_item, item_id):
        try:
            db.session.query(ItemModel).filter(ItemModel.id == item_id).update(posted_item)
            db.session.commit()
            return db.session.get(ItemModel,item_id)
        except SQLAlchemyError as e:
            abort(http_status_code=500, message="The item doesn't exist!")

    def delete(self, item_id):
        try:
            item = db.session.query(ItemModel).filter(ItemModel.id == item_id).delete()
            db.session.commit()
            if item == 0:
                return {"message": "The item not found!"},404
            return '', 204
        except SQLAlchemyError as e:
            abort(http_status_code=500, message="An error occurred!")


