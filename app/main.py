from fastapi import FastAPI
#from app.src.routes.cursor_infused.posts import posts_router
from app.src.routes.orm_infused.post import posts_router
from app.src.routes.orm_infused.auth import auth_router
from app.src.connection.orm.ormDatabase import engine
from app.src.models.models import Base
from fastapi.middleware.cors import CORSMiddleware

# ✅ Correct way to create tables from SQLAlchemy models
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or "*" for all
    allow_credentials=True,
    allow_methods=["*"],  # or specify ['POST', 'GET', 'OPTIONS']
    allow_headers=["*"],  # or specify ['Authorization', 'Content-Type']
)


@app.get("/")
def read_root():
    return {"Hello": "Welcome to my API"}


# ✅ Uncomment to activate routes
app.include_router(posts_router)
app.include_router(auth_router)
