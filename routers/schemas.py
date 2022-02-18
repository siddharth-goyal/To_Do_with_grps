from tokenize import group
from pydantic import BaseModel
from datetime import date
from typing import List


class UserBase(BaseModel):
  username: str
  email: str
  password: str

# for user display
class UserDisplay(BaseModel):
  username: str
  email: str
  class Config():
    orm_mode = True

class TodoBase(BaseModel):
  task: str
  assigned_to: str
  due_date: date
  is_completed: bool
  creator_id: int
  group_text: str
  group_id: int

# For user who assigned task Display
class User(BaseModel):
  username: str
  class Config():
    orm_mode = True

# for todo display
class TodoDisplay(BaseModel):
  id: int
  task: str
  assigned_to: str
  due_date: str
  is_completed: bool
  group_text: str
  group_id: int
  # user: User
  class Config():
    orm_mode = True

class UserAuth(BaseModel):
  id: int
  username: str
  email: str

