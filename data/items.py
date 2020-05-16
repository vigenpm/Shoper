import datetime

import sqlalchemy
from flask import jsonify
from flask_restful import Resource, abort, reqparse

from . import db_session
from .db_session import SqlAlchemyBase

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('image', required=True)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('buyer_id', required=True, type=int)


def abort_if_items_not_found(items_id):
    session = db_session.create_session()
    items = session.query(Item).get(items_id)
    if not items:
        abort(404, message=f"Item {items_id} not found")


class Item(SqlAlchemyBase):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=True)
    buyer_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=True)


class ItemsResource(Resource):
    def get(self, items_id):
        abort_if_items_not_found(items_id)
        session = db_session.create_session()
        items = session.query(Item).get(items_id)
        return jsonify({'items': items.to_dict(
            only=('name', 'image', 'user_id', 'buyer_id'))})

    def delete(self, items_id):
        abort_if_items_not_found(items_id)
        session = db_session.create_session()
        items = session.query(Item).get(items_id)
        session.delete(items)
        session.commit()
        return jsonify({'success': 'OK'})


class ItemsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        items = session.query(Item).all()
        return jsonify({'items': [item.to_dict(
            only=('name', 'image', 'user_id', 'buyer_id')) for item in items]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        items = Item(
            name=args['name'],
            image=args['image'],
            user_id=args['user_id'],
            buyer_id=args['buyer_id']
        )
        session.add(items)
        session.commit()
        return jsonify({'success': 'OK'})
