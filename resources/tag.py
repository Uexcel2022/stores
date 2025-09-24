from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema
from db import db
blp = Blueprint('tags', __name__, description='tag related operations')

@blp.route('/stores/<int:store_id>/tags')
class Tag(MethodView):
    @blp.arguments(TagSchema)
    @blp.response(200,TagSchema)
    def post(self,tag_data, store_id):
        tag = TagModel(**tag_data,store_id = store_id)
        try:
            db.session.add(tag)
            db.session.commit()
            return tag
        except IntegrityError:
            db.session.rollback()
            abort(400, message='A duplicate tag or missing parameter.')
        except SQLAlchemyError:
            db.session.rollback()
            abort(400, message='Database error')

    @blp.response(200,TagSchema(many=True))
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()


@blp.route('/tags/<int:tag_id>')
class  TagList(MethodView):
    @blp.response(200,TagSchema)
    def get(self,tag_id):
        return TagModel.query.get_or_404(tag_id)

    @blp.arguments(TagSchema)
    @blp.response(200,TagSchema)
    def put(self,tag_data, tag_id):
        try:
            db.session.query(TagModel).filter(TagModel.id == tag_id).update(tag_data)
            tag = db.session.get(TagModel, tag_id)
            if tag is None:
                db.session.rollback()
                abort(404, message="The tag not found.")
            db.session.commit()
            return tag
        except IntegrityError:
            db.session.rollback()
            abort(400, message='A duplicate tag or missing parameter.')
        except SQLAlchemyError:
            db.session.rollback()
            abort(400, message='Database Error')

    @blp.response(204)
    def delete(self,tag_id):
        try:
            res = db.session.query(TagModel).filter(TagModel.id == tag_id).delete()
            if res == 0:
                db.session.rollback()
                abort(404, message="The tag not found.")
            db.session.commit()
            return ''
        except SQLAlchemyError:
            db.session.rollback()
            abort(400, message='Database Error')


@blp.route('/item/<int:item_id>/tag/<int:tag_id>')
class LinkTagToItem(MethodView):

    @blp.response(201,TagSchema)
    def post(self,item_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
            return tag
        except SQLAlchemyError:
            abort(500, message='An error occurred while inserting an item.')

    @blp.response(200, TagSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
            return {'message':'Item removed from tag.','item':item,'tag':tag}
        except SQLAlchemyError:
            abort(500, message='An error occurred while inserting an item.')


@blp.route('/tag/<int:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag.tags.all()

    @blp.response(204, description="delete a tag if no item is tagged",
                  example={"message":"tag deleted"}
    )
    @blp.alt_response(404, description="The tag not found.")
    @blp.alt_response(400, description="When tag is tagged to one or more items.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.delete(tag)
            db.session.commit()
            return ''
        abort(400, message="Could not delete tag because it tagged one or more items.")


