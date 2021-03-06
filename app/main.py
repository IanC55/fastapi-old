
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models #, schemas, utils
from .database import engine #, get_db
from .routers import post, user, auth, vote
from .config import settings

# none of these are required
# from fastapi import Response, status, HTTPException, Depends, APIRouter
#from fastapi.params import Body
#from pydantic import BaseModel

#from random import randrange
#from pydantic.networks import PostgresDsn
#from sqlalchemy.sql.functions import mode

#from starlette.responses import Response
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
#from sqlalchemy.orm import Session


#####################################
# Create missing tables at startup
# Now performed by Alembic

# models.Base.metadata.create_all(bind=engine)
#
######################################

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




    


# my_posts = [{"title": "Title of Post 1", "content": "Content of post 1", "id": 1},
# {"title": "Favourate Foods", "content": "I like Pizza", "id": 2}]

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



     