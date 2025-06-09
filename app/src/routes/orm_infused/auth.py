from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.src.models.models import User, Role
from app.src.schemas.roleEnum import RoleEnum
from app.src.schemas.readUser import UserListResponse, UserSingleResponse, ReadUserResponse
from app.src.schemas.createUser import CreateUserRequest 
from app.src.schemas.userLogin import UserLoginRequest, UserLoginResponse
from app.src.connection.orm.ormDatabase import get_db
from app.src.utils.auth_handler import signJWT, decodeJWT
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import bleach
from app.src.utils.auth_bearer import JWTBearer
from app.src.utils.auth_handler import signJWT, decodeJWT
from app.src.schemas.userProfile import UserProfile


auth_router = APIRouter()

from pydantic import BaseModel

class CreateRoleRequest(BaseModel):
    role_name: str

@auth_router.post("/roles", status_code=status.HTTP_201_CREATED)
def create_role(payload: CreateRoleRequest, db: Session = Depends(get_db)):
    try:
        sanitized_role_name = bleach.clean(payload.role_name.strip().lower())

        existing_role = db.query(Role).filter_by(role_name=sanitized_role_name).first()
        
        if existing_role:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role already exists")

        
        if sanitized_role_name not in [r.value for r in RoleEnum]:
            raise HTTPException(status_code=406, detail="Role not recognized")


        new_role = Role(role_name=sanitized_role_name)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)

        return {"message": "Role created successfully", "role": new_role.role_name}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")

@auth_router.get("/users", response_model=UserListResponse)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return {
      "data": users,
      "status_code": status.HTTP_200_OK
    }
@auth_router.get("/users/me", dependencies=[Depends(JWTBearer())], response_model=UserProfile)
def get_user_profile(
    token_data: dict = Depends(JWTBearer()),
    db: Session = Depends(get_db)
):
    user_id = token_data.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized"
        )

    user = db.query(User).filter_by(user_id=user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "user_id": user.user_id,
        "role": str(user.role.role_name),
    }

@auth_router.get("/users/{user_id}", response_model=UserSingleResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(user_id = user_id).first()

    return {
      "data": user,
      "status_code": status.HTTP_200_OK
    }



@auth_router.post("/users/register", status_code=status.HTTP_201_CREATED, response_model=UserSingleResponse)
def create_a_user(user_payload: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        if not user_payload:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No body in the request")

        sanitized_email = bleach.clean(user_payload.email)
        sanitized_username = bleach.clean(user_payload.username)

        existing_user = db.query(User).filter_by(email=sanitized_email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="User or Email already exists")
        


        default_role = db.query(Role).filter_by(role_name="user").first()
        if not default_role:
            raise HTTPException(status_code=500, detail="Default role not found")

        new_user = User(
        username=sanitized_username,
        email=sanitized_email,
        hashed_password="",
        role_id=default_role.role_id
        )

        new_user.hash_password(user_payload.password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "data": new_user,
            "status_code": status.HTTP_201_CREATED
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email or username already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    



@auth_router.post("/users/login", response_model=UserLoginResponse)
def login_in_users(user: UserLoginRequest, db: Session = Depends(get_db)):
    try:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="The body of the request is empty"
            )
        
        sanitized_email = bleach.clean(user.email.strip().lower())
        sanitized_password = bleach.clean(user.password)

        existing_user = db.query(User).filter_by(email=sanitized_email).first()

        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid email or password"
            )

        if not existing_user.validate_password(sanitized_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid email or password"
            )
        
        # Convert user_id to string and sign JWT
        token_data = signJWT(str(existing_user.user_id))
        
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate authentication token"
            )
        
        return token_data

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
