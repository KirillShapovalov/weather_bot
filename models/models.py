from .base_model import BaseModel
from sqlalchemy import Column, types


class User(BaseModel):
    __tablename__ = 'user'

    chat_id = Column(types.Integer, primary_key=True)
    username = Column(types.String, unique=True)
