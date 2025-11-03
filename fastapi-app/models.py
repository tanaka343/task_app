from sqlalchemy import Column,Integer,String,Date,Boolean
from database import Base

class Item(Base):
  __tablename__ = "tasks"
  id = Column(Integer,primary_key=True)
  title = Column(String,nullable=False)   
  content =Column(String,nullable=True) 
  due_date  =Column(Date,nullable=True)
  completed = Column(Boolean,default=False)