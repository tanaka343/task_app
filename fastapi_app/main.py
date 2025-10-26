from fastapi import FastAPI
from schemas import ItemCreate,ItemResponse
from typing import Optional

app = FastAPI()

class Item:
    def __init__(
            self,
            id        : int,
            title     : str,
            content   : str,
            due_date  : str,
            completed : bool
    ):
        self.id = id
        self.title = title
        self.content = content
        self.due_date = due_date
        self.completed = completed

items =[
    Item(1,"kaimono","abokado","2025-10-26",False),
    Item(2,"kaimono","tamago","2025-10-26",False),
    Item(3,"kaimono","banana","2025-10-26",False)
]


@app.get("/items0",response_model=list[ItemResponse])
def find_all():
    return items

@app.get("/items/{id}",response_model=Optional[ItemResponse])
def find_by_id(id :int):
    for item in items:
        if item.id == id:
            return item
        
@app.get("/items/",response_model=Optional[ItemResponse])
def find_by_due(due_date :str):
    filterd_item=[]
    for item in items:
        if item.due_date ==due_date:
            filterd_item.append(item)
    return filterd_item

@app.post("/items",response_model=ItemResponse)
def create(create_item :ItemCreate):
    new_item= Item(
        len(items)+1,
        create_item.title,
        create_item.content,
        create_item.due_date,
        create_item.completed
    )
    items.append(new_item)
    return new_item



    


