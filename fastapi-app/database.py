"""データベース接続設定

SQLAlchemyを使用したデータベース接続とセッション管理を定義するモジュール。
FastAPIアプリケーション全体で使用するDB接続エンジン、セッション、ベースクラスを提供します。
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

# データベース接続URL（SQLiteファイルのパス）
SQL_URL = "sqlite:///../database.db"

# SQLAlchemyエンジン（DB接続を管理）
# connect_args: SQLiteで別スレッドからのアクセスを許可
engine = create_engine(SQL_URL,connect_args={"check_same_thread": False})#connect_args別のスレッドからデータベースにアクセス可能にする

# セッションファクトリ（DB操作用のセッションを生成）
# autoflush=False: 自動フラッシュを無効化
# autocommit=False: 自動コミットを無効化（明示的なcommitが必要）
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

# モデルクラスのベースクラス（全てのモデルがこれを継承）
Base = declarative_base()

def get_db():
  """データベースセッションを取得
    
    FastAPIの依存性注入で使用するDB接続セッションを提供します。
    リクエストごとに新しいセッションを作成し、処理後に自動でクローズします。
    
    Yields:
        Session: SQLAlchemyのデータベースセッション
        
    Example:
        @app.get("/items")
        def find_all(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()