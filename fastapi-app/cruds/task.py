from sqlalchemy.orm import Session
from models import Item,User
from typing import Optional
from datetime import timedelta,date
from schemas import ItemCreate, ItemUpdate

def find_all(db :Session,user_id :int):
    return db.query(Item).filter(Item.user_id == user_id).all()

def find_by_due(db :Session,due_date :str,end :Optional[int]):
    
    from_dt = date.fromisoformat(due_date)
    if end is None:
        found_items = db.query(Item).filter(Item.due_date == from_dt).all()
    else: 
        to_dt = from_dt +timedelta(days=end)
        found_items = db.query(Item).filter(Item.due_date.between(from_dt,to_dt)).order_by(Item.due_date).all()
    if not found_items:
        return None
    return found_items

def find_by_due_fromtoday(db :Session,end :Optional[int] ):
    today = date.today()
    if end is None:
        found_items = db.query(Item).filter(Item.due_date == today).all()
    else:
        to_dt = today + timedelta(days=end)
        found_items = db.query(Item).filter(Item.due_date.between(today,to_dt)).order_by(Item.due_date).all()
    
    if not found_items:
        return None
    return found_items

def find_by_id(id :int,db :Session,user_id :int):
    found_item = db.query(Item).filter(Item.id == id).filter(Item.user_id == user_id).first()
    if not found_item:
        return None
    return found_item

def create(create_item :ItemCreate,db :Session,user_id :int):
    new_item= Item(
        **create_item.model_dump(),user_id=user_id
    )
    db.add(new_item)
    db.commit()
    return new_item

def update(update_item :ItemUpdate,id :int,db :Session,user_id :int):
    item = find_by_id(id,db,user_id)
    if not item:
        return None
    item.title = item.title if update_item.title is None else update_item.title
    item.content = item.content if update_item.content is None else update_item.content
    item.due_date = item.due_date if update_item.due_date is None else update_item.due_date
    item.completed = item.completed if update_item.completed is None else update_item.completed
    db.add(item)
    db.commit()
    return item

def delete(id :int,db :Session,user_id :int):
    item = find_by_id(id,db,user_id)
    if not item:
       return None
    db.delete(item)
    db.commit()
    return item