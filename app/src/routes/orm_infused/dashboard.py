from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.src.connection.orm.ormDatabase import get_db
from app.src.models.models import User, Dashboard
from app.src.schemas.createDashboard import ReadDashboardResponse
from app.src.utils.auth_bearer import JWTBearer

dashbord_router = APIRouter()

@dashbord_router.post("/dashboard/{user_id}", response_model=ReadDashboardResponse)
def create_user_dashboard(user_id: int, db: Session = Depends(get_db)):

    # ✅ Check if user exists
    user = db.query(User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # ✅ Check if dashboard already exists
    dashboard = db.query(Dashboard).filter_by(owner_id=user_id).first()
    if dashboard:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Dashboard already exists"
        )
    
    # ✅ Create and persist new dashboard
    new_dashboard = Dashboard(owner_id=user.user_id)
    db.add(new_dashboard)
    db.commit()
    db.refresh(new_dashboard)

    return {
        "dashboard_id": new_dashboard.dashboard_id,
        "owner_id": new_dashboard.owner_id
    }

@dashbord_router.get("/dashboard", dependencies=[Depends(JWTBearer())], response_model=ReadDashboardResponse)
def get_user_dashboard(token_data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):
    user_id = token_data.get("user_id")

    user = db.query(User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    dashboard = db.query(Dashboard).filter_by(owner_id=user_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    return dashboard

