"""データベースモデル定義

タスク管理アプリのデータベーステーブル構造を定義するモジュール。
SQLAlchemyのORMを使用してPythonクラスとデータベーステーブルをマッピングします。
"""

from sqlalchemy import Column,Integer,String,Date,Boolean
from database import Base

class Item(Base):
  """タスク管理のデータモデル
    
    タスクの情報を保存するためのSQLAlchemyモデルクラス。
    データベースのtasksテーブルに対応します。
    
    Attributes:
        id: タスクの一意識別子（主キー）
        title: タスクのタイトル（必須）
        content: タスクの詳細内容（任意）
        due_date: タスクの期限日（任意）
        completed: タスクの完了状態（デフォルト: False）
  """
  __tablename__ = "tasks"
  id = Column(Integer,primary_key=True)
  title = Column(String,nullable=False)   
  content =Column(String,nullable=True) 
  due_date  =Column(Date,nullable=True)
  completed = Column(Boolean,default=False)