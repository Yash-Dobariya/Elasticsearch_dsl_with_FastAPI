from pydantic import BaseModel
import uuid


class RequestUser(BaseModel):
    """validation user"""

    first_name: str
    last_name: str
    user_name: str
    password: str
    email_id: str


class ResponseUser(BaseModel):
    id: str
    first_name: str
    last_name: str
    user_name: str
    email_id: str
