from fastapi import FastAPI,Depends,Query,HTTPException
from schemas import ItemCreate,ItemResponse
from typing import Optional
from models import Item
from database import get_db
from sqlalchemy.orm import Session
from datetime import date,timedelta

app = FastAPI()

# class Item:
#     def __init__(
#             self,
#             id        : int,
#             title     : str,
#             content   : str,
#             due_date  : str,
#             completed : bool
#     ):
#         self.id = id
#         self.title = title
#         self.content = content
#         self.due_date = due_date
#         self.completed = completed

# items =[
#     Item(1,"kaimono","abokado","2025-10-26",False),
#     Item(2,"kaimono","tamago","2025-10-26",False),
#     Item(3,"kaimono","banana","2025-10-26",False)
# ]


@app.get("/items",response_model=list[ItemResponse])
def find_all(db :Session = Depends(get_db)):
    return db.query(Item).all()



@app.get("/items/",response_model=list[ItemResponse])
def find_by_due(due_date :str = Query(example="2025-10-30"),end :Optional[int] = Query(default=None,example=7),db :Session=Depends(get_db)):
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





@app.get("/items/today",response_model=list[ItemResponse])
def find_by_due_fromtoday(end :Optional[int] = Query(default=None,example=7),db : Session=Depends(get_db)):
    today = date.today()
    if end is None:
        found_items = db.query(Item).filter(Item.due_date == today.date()).all()
    else:
        to_dt = today + timedelta(days=end)
        found_items = db.query(Item).filter(Item.due_date.between(today,to_dt)).order_by(Item.due_date).all()
    
    if not found_items:
        raise HTTPException(status_code=404,detail="Task not found")
    return found_items

@app.get("/items/{id}",response_model=Optional[ItemResponse])
def find_by_id(id :int,db :Session = Depends(get_db)):
    found_item = db.query(Item).filter(Item.id == id).first()
    if not found_item:
        raise HTTPException(status_code=404,detail="Task not found")
    return found_item


@app.post("/items",response_model=ItemResponse)
def create(create_item :ItemCreate,db :Session = Depends(get_db)):
    new_item= Item(
        **create_item.model_dump()
    )
    db.add(new_item)
    db.commit()
    return new_item



    


