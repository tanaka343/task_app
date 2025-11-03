from fastapi import FastAPI,Depends,Query,HTTPException
from schemas import ItemCreate,ItemResponse,ItemUpdate
from typing import Optional
from models import Item
from database import get_db
from sqlalchemy.orm import Session
from datetime import date,timedelta
from starlette import status

app = FastAPI()


@app.get("/items",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
def find_all(db :Session = Depends(get_db)):
    return db.query(Item).all()



@app.get("/items/",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
def find_by_due(due_date :str = Query(examples=["2025-10-30"]),end :Optional[int] = Query(default=None,examples=[7]),db :Session=Depends(get_db)):
    try:    
        from_dt = date.fromisoformat(due_date)
    except ValueError:
        raise HTTPException(status_code=400,detail="nvalid date format. Use YYYY-MM-DD")

    if end is None:
        found_items = db.query(Item).filter(Item.due_date == from_dt).all()
    else: 
        to_dt = from_dt +timedelta(days=end)
        found_items = db.query(Item).filter(Item.due_date.between(from_dt,to_dt)).order_by(Item.due_date).all()
    if not found_items:
        raise HTTPException(status_code=404,detail="Task not found")
    
    return found_items





@app.get("/items/today",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
def find_by_due_fromtoday(end :Optional[int] = Query(default=None,examples=[7]),db : Session=Depends(get_db)):
    today = date.today()
    if end is None:
        found_items = db.query(Item).filter(Item.due_date == today.date()).all()
    else:
        to_dt = today + timedelta(days=end)
        found_items = db.query(Item).filter(Item.due_date.between(today,to_dt)).order_by(Item.due_date).all()
    
    if not found_items:
        raise HTTPException(status_code=404,detail="Task not found")
    return found_items


@app.get("/items/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
def find_by_id(id :int,db :Session = Depends(get_db)):
    found_item = db.query(Item).filter(Item.id == id).first()
    if not found_item:
        raise HTTPException(status_code=404,detail="Task not found")
    return found_item


@app.post("/items",response_model=ItemResponse,status_code=status.HTTP_201_CREATED)
def create(create_item :ItemCreate,db :Session = Depends(get_db)):
    new_item= Item(
        **create_item.model_dump()
    )
    db.add(new_item)
    db.commit()
    return new_item


@app.put("/items/{id}",response_model=ItemResponse,status_code=status.HTTP_200_OK)
def update(update_item :ItemUpdate,id :int,db :Session =Depends(get_db)):
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(status_code=404,detail="Task not found")

    item.title = item.title if update_item.title is None else update_item.title
    item.content = item.content if update_item.content is None else update_item.content
    item.due_date = item.due_date if update_item.due_date is None else update_item.due_date
    item.completed = item.completed if update_item.completed is None else update_item.completed

    db.add(item)
    db.commit()
    return item

@app.delete("/items/{id}",status_code=status.HTTP_200_OK)
def delete(id :int,db :Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(status_code=404,detail="Task not found")
    db.delete(item)
    db.commit()
    return item

    


