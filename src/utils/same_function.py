import uuid
from datetime import datetime


def current_datetime():
    """current date and time"""
    return str(datetime.utcnow())


def common_field():
    """common field of all indexes"""
    _uuid = str(uuid.uuid4())
    return {
        "id": _uuid,
        "created_by": _uuid,
        "updated_by": _uuid,
        "created_at": current_datetime(),
        "updated_at": current_datetime(),
    }
