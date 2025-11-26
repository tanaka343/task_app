"""データ検証スキーマ定義

FastAPIのリクエスト/レスポンスで使用するPydanticスキーマを定義するモジュール。
データのバリデーション、シリアライゼーション、ドキュメント生成に使用されます。
"""
from pydantic import BaseModel,Field,ConfigDict
from datetime import date
from typing import Optional


class ItemCreate(BaseModel):
        """タスク作成用スキーマ
        
        新規タスクを作成する際のリクエストボディの構造を定義します。
        全てのフィールドが必須です。
        
        Attributes:
            title: タスクのタイトル（2〜20文字）
            content: タスクの詳細内容（2〜20文字）
            due_date: タスクの期限日
            completed: タスクの完了状態
        """
        title     : str = Field(min_length=2,max_length=20,examples=["買い物"])
        content   : str = Field(min_length=2,max_length=20,examples=["アボカド"])
        due_date  : date = Field(examples=["2025-10-26"])
        completed : bool = Field(examples=[False])


class ItemResponse(BaseModel):
        """タスクレスポンス用スキーマ
        
        APIからタスク情報を返却する際のレスポンスボディの構造を定義します。
        データベースから取得したItemモデルを自動変換します。
        
        Attributes:
            id: タスクの一意識別子
            title: タスクのタイトル（2〜20文字）
            content: タスクの詳細内容（2〜20文字）
            due_date: タスクの期限日（任意）
            completed: タスクの完了状態
        """
        id : int
        title     : str = Field(min_length=2,max_length=20,examples=["買い物"])
        content   : str = Field(min_length=2,max_length=20,examples=["アボカド"])
        due_date  : Optional[date] = Field(default=None,examples=["2025-10-26"])
        completed : bool = Field(examples=[False])

        model_config = ConfigDict(from_attributes=True)


class ItemUpdate(BaseModel):
        """タスク更新用スキーマ
        
        既存タスクを更新する際のリクエストボディの構造を定義します。
        全てのフィールドが任意で、送信されたフィールドのみ更新されます。
        
        Attributes:
            title: タスクのタイトル（2〜20文字、任意）
            content: タスクの詳細内容（2〜20文字、任意）
            due_date: タスクの期限日（任意）
            completed: タスクの完了状態（任意）
        """
        title     : Optional[str] = Field(default=None,min_length=2,max_length=20,examples=["買い物"])
        content   : Optional[str] = Field(default=None,min_length=2,max_length=20,examples=["アボカド"])
        due_date  : Optional[date] = Field(default=None,examples=["2025-10-26"])
        completed : Optional[bool] = Field(default=None,examples=[False])

class UserCreate(BaseModel):
        username : str = Field(min_length=2,examples=["user1"])
        password : str = Field(min_length=8,examples=["test1234"])

class UserResponse(BaseModel):
        id : int = Field(gt=0,examples=["1"])
        username : str = Field(min_length=2,examples=["user1"])

class Token(BaseModel):
        access_token : str
        token_type : str

class DecodedToken(BaseModel):
        username : str
        user_id : int