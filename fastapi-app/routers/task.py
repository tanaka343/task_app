from fastapi import APIRouter,Depends
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from models import Item
from schemas import ItemResponse,ItemCreate,ItemUpdate
from starlette import status
from fastapi import FastAPI,Depends,Query,HTTPException
from schemas import ItemCreate,ItemResponse,ItemUpdate,DecodedToken
from typing import Optional,Annotated
from models import Item
from database import get_db
from sqlalchemy.orm import Session
from datetime import date,timedelta
from starlette import status
from cruds import task as task_cruds,auth as auth_cruds

router = APIRouter(prefix="/tasks",tags=["tasks"])

DbDependency = Annotated[Session,Depends(get_db)]
UserDependency = Annotated[DecodedToken,Depends(auth_cruds.get_current_user)]

@router.get("",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
async def find_all(db :DbDependency,user :UserDependency):
    """全タスクを取得
    
    タスク管理アプリに登録されている全てのタスクを取得します。
    
    Args:
        db: データベースセッション
        
    Returns:
        list[ItemResponse]: 全タスクのリスト
    """
    return task_cruds.find_all(db,user.user_id)


@router.get("/",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
async def find_by_due(db :DbDependency,due_date :str = Query(example="2025-10-30"),end :Optional[int] = Query(default=None,example=7)):
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
        found_items = task_cruds.find_by_due(db,due_date,end)
    except ValueError:
        raise HTTPException(status_code=400,detail="nvalid date format. Use YYYY-MM-DD")
    if not found_items:
        raise HTTPException(status_code=404,detail="Task not found")
    return found_items

@router.get("/today",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
async def find_by_due_fromtoday(db :DbDependency,end :Optional[int] = Query(default=None,example=7)):
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
    found_items = task_cruds.find_by_due_fromtoday(db,end)
    if not found_items:
        raise HTTPException(status_code=404,detail="Task not found")
    return found_items


@router.get("/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
async def find_by_id(id :int,db :DbDependency,user :UserDependency):
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
    found_item = task_cruds.find_by_id(id,db,user.user_id)
    if not found_item:
        raise HTTPException(status_code=404,detail="Task not found")
    return found_item


@router.post("",response_model=ItemResponse,status_code=status.HTTP_201_CREATED)
async def create(create_item :ItemCreate,db :DbDependency,user :UserDependency):
    """新規タスクを作成
    
    リクエストボディで受け取ったデータから新しいタスクを作成します。
    
    Args:
        create_item: 作成するタスクの情報
        db: データベースセッション
        
    Returns:
        ItemResponse: 作成されたタスク
    """
    new_item = task_cruds.create(create_item,db,user.user_id)
    return new_item


@router.put("/{id}",response_model=ItemResponse,status_code=status.HTTP_200_OK)
async def update(update_item :ItemUpdate,id :int,db :DbDependency,user :UserDependency):
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
    update_item = task_cruds.update(update_item,id,db,user.user_id)
    if not update_item:
        raise HTTPException(status_code=404,detail="Task not found")
    return update_item

@router.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete(id :int,db :DbDependency,user :UserDependency):
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
    delete_item = task_cruds.delete(id,db,user.user_id)
    if not delete_item:
        raise HTTPException(status_code=404,detail="Task not found")
    return delete_item