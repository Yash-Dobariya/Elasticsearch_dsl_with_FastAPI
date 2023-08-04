from elasticsearch_dsl import Text


class DBField:
    """same felid in all index"""
    created_at = Text()
    created_by = Text()
    updated_at = Text()
    updated_by = Text()
    is_activate = Text(default=True)
    is_deleted = Text(default=False)
