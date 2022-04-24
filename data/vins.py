import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Vinils(SqlAlchemyBase):
    __tablename__ = 'vinils'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    car_type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    #img = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=False)
