from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from src.crud.schemas import RequestUser, ResponseUser
from src.crud.model import User
from src.utils.same_function import common_field, current_datetime
from elasticsearch_dsl import Search


user = APIRouter()

INDEX_NAME = "user"


@user.post("/create_user")
def create_user(users: RequestUser):
    """Create users"""

    common_data = common_field()
    user_doc = User(
        first_name=users.first_name,
        last_name=users.last_name,
        user_name=users.user_name,
        password=users.password,
        email_id=users.email_id,
        **common_data,
    )
    user_doc.save()

    user_data = user_doc.to_dict()
    response_user_instance = ResponseUser(**user_data)
    response_data = response_user_instance.model_dump()

    return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)


@user.get("/all_users")
def all_users(page: int = 1, page_size: int = 10):
    """Get paginated list of users"""

    index = Search(index=INDEX_NAME)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    response = index[start_idx:end_idx].execute()

    users = []
    for hit in response:
        user_data = hit.to_dict()
        user_entry = {
            "document_id": hit.meta.id,
            "user_id": user_data.get("id"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "user_name": user_data.get("user_name"),
            "email_id": user_data.get("email_id"),
            "created_at": user_data.get("created_at"),
            "created_by": user_data.get("created_by"),
            "updated_at": user_data.get("updated_at"),
            "updated_by": user_data.get("updated_by"),
        }

        users.append(user_entry)

    return users


@user.get("/user/{user_id}/profile")
async def get_user(user_id: str):
    """Get a particular user from Elasticsearch by user ID"""

    index = Search(index=INDEX_NAME)
    query_detail = {"match": {"id": user_id}}
    response = index.query(query_detail).execute()

    _user = {}
    for hit in response:
        user_data = hit.to_dict()
        _user = {
            "document_id": hit.meta.id,
            "user_id": user_data.get("id"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "user_name": user_data.get("user_name"),
            "email_id": user_data.get("email_id"),
        }

    if not _user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return JSONResponse(content=_user, status_code=status.HTTP_200_OK)


@user.get("/documents/{document_id}")
def get_user_by_doc_id(document_id: str):
    """Get a particular user from Elasticsearch by document ID"""

    user_doc = User.get(id=document_id)

    if user_doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_data = {
        "document_id": user_doc.meta.id,
        "user_id": user_doc.id,
        "first_name": user_doc.first_name,
        "last_name": user_doc.last_name,
        "user_name": user_doc.user_name,
        "email_id": user_doc.email_id,
    }

    return JSONResponse(content={"user": user_data}, status_code=status.HTTP_200_OK)


@user.put("/update_user/{user_id}")
def update_user(users: dict, user_id: str):
    """Update a user by user_id"""

    user_docs = User.search().filter("match", id=user_id).execute()

    if not user_docs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_doc = user_docs[0]

    if users.get("first_name"):
        user_doc.first_name = users.get("first_name")
    if users.get("last_name"):
        user_doc.last_name = users.get("last_name")
    if users.get("password"):
        user_doc.password = users.get("password")
    if users.get("user_name"):
        user_doc.user_name = users.get("user_name")
    if users.get("email_id"):
        user_doc.email_id = users.get("email_id")

    user_doc.updated_at = current_datetime()
    user_doc.save()

    return JSONResponse(
        content=f"{user_id} updated successfully", status_code=status.HTTP_200_OK
    )


@user.delete("/delete_user/{user_id}")
def delete_user(user_id):
    user_docs = User.search().filter("match", id=user_id).execute()

    if not user_docs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_doc = user_docs[0]
    user_doc.delete()

    return JSONResponse(
        content=f"{user_id} deleted successfully", status_code=status.HTTP_200_OK
    )
