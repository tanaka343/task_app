# FastAPI版 タスク管理アプリ

FastAPIとSQLAlchemyを使用したタスク管理APIです。学習用のため、フォルダを極力分けずにシンプルに作成しました。

## 機能

- タスクのCRUD操作
- 日付範囲でのタスク検索
- 今日から指定日数後までのタスク取得
- 自動生成されるAPIドキュメント（Swagger UI）
- データベースマイグレーション管理（Alembic）
- APIテスト（pytest）

## 技術スタック

FastAPI\
SQLAlchemy（ORM）\
Alembic（マイグレーション）\
SQLite\
Pydantic（バリデーション）\
pytest（テスト）

## ファイル構成

```python
fastapi_app/
├── migrations/        # Alembicマイグレーションファイル
├── tests/             # テストファイル
├── __init__.py
├── alembic.ini        # Alembic設定
├── database.py        # データベース接続
├── main.py            # アプリケーションエントリポイント
├── models.py          # SQLAlchemyモデル
├── schemas.py         # Pydanticスキーマ
├── seed.py            # テストデータ投入スクリプト
├── test_data.csv      # テストデータ
└── requirements.txt   # 依存パッケージ
```

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. データベースのセットアップ

```bash
#マイグレーション実行（テーブル作成）
alembic upgrade head
```

### 3. （オプション）テストデータの投入

```bash
python seed.py
```

### 実行方法

```bash
uvicorn main:app --reload
```

アプリケーションが起動したら、以下のURLにアクセスできます：

- **API**: <http://localhost:8000>
- **Swagger UI**: <http://localhost:8000/docs>

### テストの実行
```bash
pytest tests/test_main.py
```

- fixtureを使ったテスト用データベースのセットアップ
- 各エンドポイントの正常系テスト
- 各エンドポイントの異常系テスト

## API仕様

### タスクのデータ構造

```json
{
  "id": 1,
  "title": "タスクのタイトル",
  "content": "タスクの内容",
  "due_date": "2025-10-30",
  "completed": false
}
```

### エンドポイント一覧

#### 1. 全タスク取得

```bash
GET /items
```

レスポンス: タスクの配列

#### 2.日付範囲でタスク取得

```bash
GET /items/?due_date=2025-10-30&end=7
```

クエリパラメータ:

- due_date (必須): 開始日（YYYY-MM-DD形式）\
- end (オプション): 開始日から何日後までを取得するか

例:

- GET /items/?due_date=2025-10-30 - 2025-10-30のタスクのみ
- GET /items/?due_date=2025-10-30&end=7 - 2025-10-30から7日間のタスク

#### 3.今日から指定日数後までのタスク取得

```bash
GET /items/today?end=7
```

クエリパラメータ:

- end (オプション): 今日から何日後までを取得するか

例:

- GET /items/today - 今日のタスクのみ\
- GET /items/today?end=7 - 今日から7日間のタスク

#### 4. ID指定でタスク取得

```bash
GET /items/{id}
```

#### 5. タスク作成

```bash
POST /items
```

リクエストボディ:

```json
{
  "title": "新しいタスク",
  "content": "タスクの詳細",
  "due_date": "2025-11-01",
  "completed": false
}
```

#### 6. タスク更新

```bash
PUT /items/{id}
```

リクエストボディ: 更新したいフィールドのみ指定可能

```json
{
  "title": "更新されたタイトル",
  "completed": true
}
```

#### 7. タスク削除

```bash
DELETE /items/{id}
```

## 開発のポイント

- SQLAlchemyの使用\
    直接SQLを書く代わりに、Pythonのクラスとメソッドでデータベース操作を行います。
- Alembicによるマイグレーション管理\
データベーススキーマの変更履歴を管理し、バージョン管理が可能です。
- 自動バリデーション\
Pydanticスキーマにより、リクエストとレスポンスのデータが自動的に検証されます。
- 自動ドキュメント生成\
Swagger UIにより、APIの仕様とテストが簡単に行えます。
- APIテストの実装
fixtureを使ってテスト用データベースのセットアップを行い、各エンドポイントの正常系・異常系テストを作成しました。
