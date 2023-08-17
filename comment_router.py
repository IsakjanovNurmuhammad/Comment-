from fastapi import Depends, HTTPException, APIRouter

from db import get_db, SessionLocal
from models import Comment, User
from schemas import CommentSchema, comment_read
from typing import List

router = APIRouter()


@router.get("/all-comments", response_model=List[comment_read])
async def get_all_comments(db: SessionLocal = Depends(get_db)):
    query = db.query(Comment).all()
    return query


@router.get("/comment/{id}", response_model=comment_read)
async def get_comment(id:int,
                      db: SessionLocal = Depends(get_db)):
    query = db.query(Comment).filter(Comment.id == id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        return query


@router.post("/new-comment", response_model=comment_read)
async def add_comment(schema: CommentSchema,
                      db: SessionLocal = Depends(get_db)):
    model = Comment()
    query = db.query(User).filter(User.id == schema.user_id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        model.comment = schema.comment
        model.user_id = schema.user_id

        db.add(model)
        db.commit()
        return model


@router.put("/edit-comment", response_model=comment_read)
async def edit_comment(id:int,
                       schema: CommentSchema,
                       db: SessionLocal = Depends(get_db),
                       ):

    model = db.query(Comment).filter(Comment.id == id).first()

    if model is None:
        raise HTTPException(status_code=404, detail="Not found")
    else:
        model.comment = schema.comment

        db.add(model)
        db.commit()

        return model


@router.delete("/del-comment/{id}")
async def del_comment(id: int,
                      db: SessionLocal = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Not found")
    else:
        db.delete(comment)
        db.commit()
        return "Successfully deleted"