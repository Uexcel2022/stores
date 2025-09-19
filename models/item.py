from enum import unique

from db import db

class ItemModel(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False,unique=True)
    price = db.Column(db.Float(precision=2),nullable=False,unique=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False, unique=False)
    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship('TagModel',back_populates="items", secondary='item_tag', lazy=True)