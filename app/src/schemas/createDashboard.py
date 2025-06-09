from pydantic import BaseModel


class CreateDashboardResponse(BaseModel):
     dashboard_id: int
     owner_id: int

class ReadDashboardResponse(BaseModel):
     dashboard_id: int
     owner_id: int
