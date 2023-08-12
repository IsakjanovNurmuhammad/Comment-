from fastapi import FastAPI
from db import Base, engine
from user_router import router as user_router
from comment_router import router as comment_router


app = FastAPI()
app.include_router(comment_router,tags=['Comment'])
app.include_router(user_router,tags=['User'])

Base.metadata.create_all(engine)

