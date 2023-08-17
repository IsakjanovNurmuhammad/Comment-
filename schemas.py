from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    email: str
    password: str


class user_read(BaseModel):
    id: int
    name: str
    email: str


class CommentSchema(BaseModel):
    user_id: int
    comment: str


class comment_read(BaseModel):
    id: int
    user_id: int
    comment: str
