from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
from secrets import token_hex
from db import get_db, SessionLocal
from models import Comment, User, Comment_image
from schemas import CommentSchema, comment_read
from typing import List
router = APIRouter()

@router.get("/all-images")
async def all_images(db: SessionLocal = Depends(get_db)):
    images = db.query(Comment_image).all()
    return images
@router.get("/get_image")
async def get_image_by_comment_id(comment_id: int,
                                  db: SessionLocal = Depends(get_db)):
    query = db.query(Comment_image).filter(Comment_image.comment_id == comment_id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return query

@router.post("/add-image")
async def add_image(comment_id: int,
                    image: UploadFile = File(...),
                    db: SessionLocal = Depends(get_db)):
    query = db.query(Comment).filter(Comment.id == comment_id).first()
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

@router.delete("/delete_image")
async def del_image(comment_id: int,
                    db: SessionLocal = Depends(get_db)):
    query = db.query(Comment_image).filter(Comment_image.comment_id == comment_id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(query)
    db.commit()
    return "Image successfully deleted."