
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

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

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self,posted_item):
       item = ItemModel(**posted_item)
       try:
           db.session.add(item)
           db.session.commit()
           return item
       except IntegrityError as e:
            abort(http_status_code=409,message="An item with same name already exists.")
       except SQLAlchemyError as e:
            abort(http_status_code=500,message="An error occurred while inserting an item.")

@blp.route('/stores/<int:item_id>/items')
class ItemList(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
            return ItemModel.query.get_or_404(item_id)

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, posted_item, item_id):
        try:
            db.session.query(ItemModel).filter(ItemModel.id == item_id).update(posted_item)
            db.session.commit()
            item = db.session.get(ItemModel,item_id)
            if item is None:
                abort(404,message='The item not found.')
            return item
        except IntegrityError as e:
            abort(http_status_code=409, message="An item with same name already exists.")

    @jwt_required(fresh=True)
    def delete(self, item_id):
        try:
            item = db.session.query(ItemModel).filter(ItemModel.id == item_id).delete()
            db.session.commit()
            if item == 0:
                return {"message": "The item not found!"},404
            return '', 204
        except SQLAlchemyError as e:
            abort(http_status_code=500, message="An error occurred!")


