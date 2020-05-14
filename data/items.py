import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Item(SqlAlchemyBase):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    buyer_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
