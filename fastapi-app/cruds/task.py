from sqlalchemy.orm import Session
from models import Item,User
from typing import Optional
from datetime import timedelta,date
from schemas import ItemCreate, ItemUpdate

def find_all(db :Session,user_id :int):
    """ユーザーの全タスクを取得
    
    指定されたユーザーIDに紐づく全てのタスクをデータベースから取得します。
    
    Args:
        db: データベースセッション
        user_id: 取得対象のユーザーID
        
    Returns:
        list[Item]: タスクのリスト（空の場合は空リスト）
    """
    return db.query(Item).filter(Item.user_id == user_id).all()

def find_by_due(db :Session,due_date :str,end :Optional[int]):
    """期限日範囲でタスクを検索
    
    due_dateをdate型に変換し、endが指定されていれば範囲検索、
    指定されていなければ完全一致でフィルタリングします。
    
    Args:
        db: データベースセッション
        due_date: 検索開始日（YYYY-MM-DD形式の文字列）
        end: 検索終了日までの日数（Noneの場合は完全一致）
        
    Returns:
        list[Item]: 検索条件に一致するタスクのリスト
        None: タスクが見つからない場合
        
    Raises:
        ValueError: due_dateの形式が不正な場合
    """
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
    """今日から期限日範囲でタスクを検索
    
    検索日当日の日付で、endが指定されていれば範囲検索、
    指定されていなければ今日のタスクのみ検索します。
    
    Args:
        db: データベースセッション
        end: 検索終了日までの日数（Noneの場合は完全一致）
        
    Returns:
        list[Item]: 検索条件に一致するタスクのリスト
        None: タスクが見つからない場合
        
    """
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
    """idでタスクを検索
    
    指定されたユーザーIDに紐づき、idの一致するタスクをデータベースから取得します。

    Args:
        id: タスクID
        db: データベースセッション
        user_id: 取得対象のユーザーID
        
    Returns:
        Item: 検索条件に一致するタスク
        None: タスクが見つからない場合
        
    """
    found_item = db.query(Item).filter(Item.id == id).filter(Item.user_id == user_id).first()
    if not found_item:
        return None
    return found_item

def create(create_item :ItemCreate,db :Session,user_id :int):
    """新規タスクを作成
    
    リクエストデータから新しいタスクを作成し、データベースに追加

    Args:
        create_item: ItemCreateスキーマ
        db: データベースセッション
        user_id: 作成対象のユーザーID
        
    Returns:
        Item: 新しく作成したタスク
    """
    new_item= Item(
        **create_item.model_dump(),user_id=user_id
    )
    db.add(new_item)
    db.commit()
    return new_item

def update(update_item :ItemUpdate,id :int,db :Session,user_id :int):
    """タスクを更新
    
    指定されたユーザーIDとidに紐づき、タスクをデータベースから取得し、送信されたフィールドのみ更新

    Args:
        update_item: ItemUpdateスキーマ
        id: タスクのid
        db: データベースセッション
        user_id: 更新対象のユーザーID
        
    Returns:
        Item: 更新したタスク
        None: タスクが見つからない場合
    """
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
    """タスクを削除
    
    指定されたユーザーIDとidに紐づき、タスクをデータベースから取得し、データベースから削除

    Args:
        id: タスクのid
        db: データベースセッション
        user_id: 削除対象のユーザーID
        
    Returns:
        Item: 削除したタスク
        None: タスクが見つからない場合
    """
    item = find_by_id(id,db,user_id)
    if not item:
       return None
    db.delete(item)
    db.commit()
    return item