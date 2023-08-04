import uuid
from elasticsearch_dsl import Document, Text
from src.utils.same_model import DBField

def default_uuid():
    return uuid.uuid4()


class User(DBField, Document):
    """create user index"""
    class Index:
        name = "user"

    id = Text()
    first_name = Text()
    last_name = Text()
    user_name = Text()
    password = Text()
    email_id = Text()
