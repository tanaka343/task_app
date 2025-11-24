from fastapi import FastAPI,Depends,Query,HTTPException
from schemas import ItemCreate,ItemResponse,ItemUpdate
from typing import Optional,Annotated
from models import Item
from database import get_db
from sqlalchemy.orm import Session
from datetime import date,timedelta
from routers import task
from starlette import status

DbDependency = Annotated[Session,Depends(get_db)]
app = FastAPI()

app.include_router(task.router)












    


