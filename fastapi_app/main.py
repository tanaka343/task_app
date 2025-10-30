from fastapi import FastAPI,Depends
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

@app.get("/items/{id}",response_model=Optional[ItemResponse])
def find_by_id(id :int,db :Session = Depends(get_db)):
    return db.query(Item).filter(Item.id == id).first()


@app.get("/items/",response_model=list[ItemResponse])
def find_by_due(due_date :str = Query(example="2025-10-30"),end :Optional[int] = Query(default=None,example=7),db :Session=Depends(get_db)):
    if end is None:
        return db.query(Item).filter(Item.due_date == due_date).all()
    else:
        tasklist=[]
        from_dt = date.fromisoformat(due_date)
        # to_dt = from_dt + timedelta(days=end)
        # return db.query(Item).filter(from_dt <= Item.due_date <=to_dt).all()
        for i in range(end+1):
            due = from_dt +timedelta(days=i)
            tasklist.extend(db.query(Item).filter(Item.due_date==due).all())
        return tasklist

@app.post("/items",response_model=ItemResponse)
def create(create_item :ItemCreate,db :Session = Depends(get_db)):
    new_item= Item(
        **create_item.model_dump()
    )
    db.add(new_item)
    db.commit()
    return new_item


# @app.get("/items/", response_model=list[ItemResponse])
# def find_by_due(due_date: str, end: Optional[int] = None, db: Session = Depends(get_db)):
#     from_dt = date.fromisoformat(due_date)

#     if end is None:
#         return db.query(Item).filter(Item.due_date == from_dt).all()
#     else:
#         to_dt = from_dt + timedelta(days=end)
#         # ✅ SQLAlchemyの between を使う！
#         return db.query(Item).filter(Item.due_date.between(from_dt, to_dt)).all()



    


