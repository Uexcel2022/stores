from db import db
class ItemTag(db.Model):
    __tablename__ = 'item_tag'
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'),nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'),nullable=False)