import json

from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
from secrets import token_hex
from fastapi.responses import FileResponse
from db import get_db, SessionLocal
from models import Comment, User, Comment_image
from schemas import CommentSchema, comment_read
from typing import List

router = APIRouter()
path = r"C:\Users\Mr_IT\PycharmProjects\pythonProject3"


@router.get("/all-comments", )
async def get_all_comments(db: SessionLocal = Depends(get_db)):
    comments = db.query(Comment).all()
    return comments


@router.get("/comment/{id}")
async def get_comment(id:int,
                      db: SessionLocal = Depends(get_db)):
    query = db.query(Comment).filter(Comment.id == id).first()
    image = db.query(Comment_image).filter(Comment_image.comment_id == id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="Comment not Found")
    else:
        if image is None:
            return query
        else:
            model = comment_read()
            model.comment = query.get("comment")
            model.user_id = query.user_id
            model.id = image.image_id
            model.file_path = image.file_path
            model.file_name = image.file_name

            return model



@router.post("/new-comment", response_model=comment_read)
async def add_comment(comment: CommentSchema,
                      db: SessionLocal = Depends(get_db),
                      ):
    model = Comment()
    query = db.query(User).filter(User.id == comment.user_id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        model.comment = comment.comment
        model.user_id = comment.user_id
        db.add(model)
        db.commit()
        return model

@router.put("/add-image")
async def add_image(comment_id: int,
                    image: UploadFile = File(...),
                    db: SessionLocal = Depends(get_db)):
    query = db.query(Comment).filter(Comment.id == comment_id).first
    if query is None:
        raise HTTPException(status_code=404, detail="Comment not found.")
    file_ext = image.filename.split(".").pop()
    file_name = token_hex(10)
    file_path = f"{file_name}.{file_ext}"
    with open(file_path, "wb") as f:
        content = await image.read()
        f.write(content)
    model = Comment_image()
    model.comment_id = comment_id
    model.file_path = file_path
    model.file_name =file_name

    db.add(model)
    db.commit()
    return "Successfully added"


@router.put("/edit-comment", response_model=comment_read)
async def edit_comment(id:int,
                       schema: CommentSchema,
                       db: SessionLocal = Depends(get_db),
                       ):

    model = db.query(Comment).filter(Comment.id == id).first()

    if model is None:
        raise HTTPException(status_code=404, detail="Comment not found")
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
        raise HTTPException(status_code=404, detail="Comment not found")
    else:
        db.delete(comment)
        db.commit()
        return "Successfully deleted"