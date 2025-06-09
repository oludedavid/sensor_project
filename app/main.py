from fastapi import FastAPI
#from app.src.routes.cursor_infused.posts import posts_router
from app.src.routes.orm_infused.post import posts_router
from app.src.routes.orm_infused.auth import auth_router
from app.src.connection.orm.ormDatabase import engine
from app.src.models.models import Base

# ✅ Correct way to create tables from SQLAlchemy models
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Welcome to my API"}


# ✅ Uncomment to activate routes
app.include_router(posts_router)
app.include_router(auth_router)
