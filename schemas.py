from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str



class CommentCreate(BaseModel):
    comment: str
    user_id: int



class UserSchema(BaseModel):
    id: int
    name: str
    email: str



class CommentSchema(BaseModel):
    id: int
    comment: str
    user_id: int