from fastapi import APIRouter, HTTPException, Response, status, Depends
from app.src.schemas.readPost import PostSingleResponse, PostListResponse, ReadPostModel
from app.src.schemas.createPost import CreatePostRequest
from app.src.schemas.updatePost import UpdatePostRequest
from psycopg2 import Error
import bleach
from app.src.connection.orm.ormDatabase import get_db
from sqlalchemy.orm import Session
from app.src.models import models
from app.src.utils.auth_bearer import JWTBearer
from app.src.utils.auth_handler import signJWT, decodeJWT

posts_router = APIRouter()

@posts_router.get("/posts", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK, response_model=PostListResponse)
def get_all_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {
        "data": posts,
        "status_code": status.HTTP_200_OK
    }
@posts_router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostSingleResponse)
def create_post(
    post: CreatePostRequest,
    db: Session = Depends(get_db),
    token_data: dict = Depends(JWTBearer()) 
):
    user_id = token_data["user_id"]

    sanitized = bleach.clean(post.title), bleach.clean(post.content)
    new_post = models.Post(
        title=sanitized[0],
        content=sanitized[1],
        owner_id=user_id
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "data": new_post,
        "status_code": status.HTTP_201_CREATED
    }


@posts_router.get("/posts/{post_id}", dependencies=[Depends(JWTBearer())])
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    return {}
