from pydantic import BaseModel


class AddToAllowList(BaseModel):
    user_id: int
