from fastapi import Depends, HTTPException, APIRouter

from db import get_db
from models import Comment, User
from schemas import CommentSchema, CommentCreate

router = APIRouter()

@router.get("/comments/", response_model=list[CommentSchema])
async def get_users(db=Depends(get_db)):
    comm = db.query(Comment).all()
    return comm

@router.post("/comments/", response_model=CommentSchema)
async def create_comment(comment: CommentCreate, db=Depends(get_db)):
    db_comment = Comment(comment=comment.comment, user_id=comment.user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment



@router.get("/users/{user_id}/comments/", response_model=list[CommentSchema])
async def get_comments_by_user(user_id: int, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.comments



@router.put("/comments/{comment_id}")
async def update_comment(comment_id: int, comment: str, db=Depends(get_db)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db_comment.comment = comment
    db.commit()
    db.refresh(db_comment)
    return db_comment