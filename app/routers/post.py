
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts"
    , tags=["Posts"] )
    # ,tags="Posts")

# request GET and matches the path
@router.get("/")
async def root():
    return {"message": "Welcome to my API testing"}

#@router.get("/", response_model=List[schemas.Post])
#@router.get("/")
@router.get("/",  response_model=List[schemas.PostOut])

def get_posts(db:Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user),
        limit: int = 10, 
        skip: int = 0,
        search: Optional[str]=""):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post, )
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # sql =  "INSERT INTO posts (title, content, published)"
    # sql += "VALUES (%s, %s, %s) RETURNING *"
    # cursor.execute(sql, (post.title, post.content, post.published))
    # new_post = cursor.fetchone
    # conn.commit()

    #print({"User id": current_user.email})
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 

      
    
@router.get("/{id}", response_model=schemas.PostOut)
def get_posts(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # sql = f"SELECT * FROM posts WHERE id = {id}"
    # # print(sql) 
    # cursor.execute("SELECT * FROM posts WHERE id = %s" % id)
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f"Post with id: {id} was not found")
    return post   



@router.delete("/{id}")
def delete_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *" % id)
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f"Post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only authorised to delete your own posts")

    post_query.delete(synchronize_session=False)
    db.commit()                            

    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # sql =  "UPDATE posts SET title = %s, content = %s, published = %s "
    # sql += " WHERE id = %s"
    # sql += " RETURNING *"
    
    # cursor.execute(sql, (post.title, post.content, post.published, str(id)),)
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(    status_code=status.HTTP_404_NOT_FOUND,
                                detail = f"Post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only authorised to update your own posts")                                
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()