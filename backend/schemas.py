from pydantic import BaseModel

class OrderOut(BaseModel):
    id: int
    description: str
    status: str
    priority: int
    created_at: str