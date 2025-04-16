from typing import Optional

from pydantic import BaseModel, Field


class UserStateModel(BaseModel):
    full_name: str = Field(default="")
    email: str = Field(default="")
