from fastapi import FastAPI,Depends,Query,HTTPException
from schemas import ItemCreate,ItemResponse,ItemUpdate
from typing import Optional,Annotated
from models import Item
from database import get_db
from sqlalchemy.orm import Session
from datetime import date,timedelta
from starlette import status

DbDependency = Annotated[Session,Depends(get_db)]
app = FastAPI()


@app.get("/items",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
def find_all(db :DbDependency):
    """全タスクを取得
    
    タスク管理アプリに登録されている全てのタスクを取得します。
    
    Args:
        db: データベースセッション
        
    Returns:
        list[ItemResponse]: 全タスクのリスト
    """
    return db.query(Item).all()



@app.get("/items/",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
def find_by_due(db :DbDependency,due_date :str = Query(example="2025-10-30"),end :Optional[int] = Query(default=None,example=7)):
    """期限日でタスクを検索
    
    指定した期限日、または期限日から指定日数範囲内のタスクを取得します。
    endパラメータを省略すると、due_dateと完全一致するタスクのみ取得します。
    
    Args:
        due_date: 検索開始日（YYYY-MM-DD形式）
        end: 検索終了日までの日数（省略時はdue_dateのみ）
        db: データベースセッション
        
    Returns:
        list[ItemResponse]: 検索条件に一致するタスクのリスト
        
    Raises:
        HTTPException: 日付形式が不正な場合（400）、タスクが見つからない場合（404）
    """
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
def find_by_due_fromtoday(db :DbDependency,end :Optional[int] = Query(default=None,example=7)):
    """今日を起点に期限日でタスクを検索
    
    今日の日付を起点として、指定日数範囲内のタスクを取得します。
    endパラメータを省略すると、今日が期限のタスクのみ取得します。
    
    Args:
        end: 今日から何日後までのタスクを取得するか（省略時は今日のみ）
        db: データベースセッション
        
    Returns:
        list[ItemResponse]: 検索条件に一致するタスクのリスト
        
    Raises:
        HTTPException: タスクが見つからない場合（404）
    """
    today = date.today()
    if end is None:
        found_items = db.query(Item).filter(Item.due_date == today).all()
    else:
        to_dt = today + timedelta(days=end)
        found_items = db.query(Item).filter(Item.due_date.between(today,to_dt)).order_by(Item.due_date).all()
    
    if not found_items:
        raise HTTPException(status_code=404,detail="Task not found")
    return found_items


@app.get("/items/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
def find_by_id(id :int,db :DbDependency):
    """IDでタスクを取得
    
    指定されたIDに一致する単一のタスクを取得します。
    
    Args:
        id: タスクID
        db: データベースセッション
        
    Returns:
        ItemResponse: 取得したタスク
        
    Raises:
        HTTPException: タスクが見つからない場合（404）
    """
    found_item = db.query(Item).filter(Item.id == id).first()
    if not found_item:
        raise HTTPException(status_code=404,detail="Task not found")
    return found_item


@app.post("/items",response_model=ItemResponse,status_code=status.HTTP_201_CREATED)
def create(create_item :ItemCreate,db :DbDependency):
    """新規タスクを作成
    
    リクエストボディで受け取ったデータから新しいタスクを作成します。
    
    Args:
        create_item: 作成するタスクの情報
        db: データベースセッション
        
    Returns:
        ItemResponse: 作成されたタスク
    """
    new_item= Item(
        **create_item.model_dump()
    )
    db.add(new_item)
    db.commit()
    return new_item


@app.put("/items/{id}",response_model=ItemResponse,status_code=status.HTTP_200_OK)
def update(update_item :ItemUpdate,id :int,db :DbDependency):
    """タスクを更新
    
    指定されたIDのタスクを部分更新します。
    送信されたフィールドのみが更新され、省略されたフィールドは元の値を保持します。
    
    Args:
        update_item: 更新するタスクの情報（部分更新可能）
        id: 更新対象のタスクID
        db: データベースセッション
        
    Returns:
        ItemResponse: 更新後のタスク
        
    Raises:
        HTTPException: タスクが見つからない場合（404）
    """
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
def delete(id :int,db :DbDependency):
    """タスクを削除
    
    指定されたIDのタスクをデータベースから完全に削除します。
    
    Args:
        id: 削除対象のタスクID
        db: データベースセッション
        
    Returns:
        Item: 削除されたタスクの情報
        
    Raises:
        HTTPException: タスクが見つからない場合（404）
    """
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(status_code=404,detail="Task not found")
    db.delete(item)
    db.commit()
    return item

    


