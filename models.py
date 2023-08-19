from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String)





class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_rel = relationship(User, backref='users')


class Comment_image(Base):
    __tablename__ = "comment's_images"
    image_id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, nullable=False, unique=True)
    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)



