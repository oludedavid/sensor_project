from fastapi import APIRouter, HTTPException, Response, status
from app.src.connection.cursor.cursorDatabase import cursor, conn
from app.src.schemas.readPost import PostSingleResponse, PostListResponse, ReadPostModel
from app.src.schemas.createPost import CreatePostRequest
from app.src.schemas.updatePost import UpdatePostRequest
from psycopg2 import Error
import bleach

posts_router = APIRouter()


#read operations
@posts_router.get("/posts", response_model=PostListResponse)
def get_all_posts():
    try:
        cursor.execute("""
            SELECT * FROM public.posts
            ORDER BY post_id
        """)
        posts = cursor.fetchall()

        if not posts:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No posts found.")

        return  {"data": posts, "status_code": status.HTTP_200_OK}

    except Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")
    

@posts_router.get("/posts/{post_id}", response_model=PostSingleResponse)
def get_post_by_id(post_id: int):
    try:
        cursor.execute("""
            SELECT * FROM public.posts
            WHERE post_id = %s
        """, (post_id,))
        
        post = cursor.fetchone()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        return {"data": post, "status_code": status.HTTP_200_OK}

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def sanitize_post_body(title: str, content: str):
    sanitized_title = bleach.clean(title.strip())
    sanitized_content = bleach.clean(content.strip())
    return {
        "sanitized_title": sanitized_title,
        "sanitized_content": sanitized_content
    }

@posts_router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=ReadPostModel)
def create_post(post: CreatePostRequest):
    try:
        if not post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No request body provided")

        sanitized_post = sanitize_post_body(post.title, post.content)
        cleaned_post_title = sanitized_post["sanitized_title"]
        cleaned_post_content = sanitized_post["sanitized_content"]

        cursor.execute("""
            INSERT INTO public.posts (title, content)
            VALUES (%s, %s)
            RETURNING post_id, title, content, published, created_at
        """, (cleaned_post_title, cleaned_post_content))

        new_post = cursor.fetchone()
        conn.commit()

        return new_post

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    


@posts_router.put("/posts", status_code=status.HTTP_202_ACCEPTED, response_model=ReadPostModel)
def update_a_post(post: UpdatePostRequest):
    try:
        if not post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No request body provided")
        
        sanitized_post = sanitize_post_body(post.title, post.content)
        cleaned_post_title = sanitized_post["sanitized_title"]
        cleaned_post_content = sanitized_post["sanitized_content"]

        cursor.execute("""
            UPDATE public.posts
            SET title = %s,
                content = %s
            WHERE post_id = %s
            RETURNING post_id, title, content, published, created_at
        """, (cleaned_post_title, cleaned_post_content, post.post_id))

        updated_post = cursor.fetchone()
        conn.commit()

        if not updated_post:
            raise HTTPException(status_code=404, detail="Post not found")

        return updated_post

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    

@posts_router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    try:
        cursor.execute("""
            DELETE FROM public.posts
            WHERE post_id = %s
            RETURNING post_id
        """, (post_id,))

        deleted = cursor.fetchone()
        conn.commit()

        if not deleted:
            raise HTTPException(status_code=404, detail="Post not found")

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")





    
