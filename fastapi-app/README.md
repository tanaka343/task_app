# FastAPI版 タスク管理アプリ

FastAPIとSQLAlchemyを使用したタスク管理APIです。学習用のため、フォルダを極力分けずにシンプルに作成しました。

## 目的
Udemyで学習したFastAPIの内容をアウトプットする目的で、既存のタスク管理アプリを再構成しました。\
CRUD処理、バリデーション、マイグレーション、テストまでの一連の流れを通して、自分でAPI設計・実装ができるようになることを目指しました。

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

## 工夫した点・学んだこと

- ORMの活用（SQLAlchemy）\
SQL文を直接書かずにPythonコードでデータ操作を行い、保守性を高めました。

- マイグレーション管理（Alembic）\
データベーススキーマの変更をバージョン管理できるようにし、変更履歴を追跡できるようにしました。

- バリデーションの自動化（Pydantic）\
入出力データの整合性を自動でチェックし、安全なAPI設計を実現しました。

- 自動ドキュメント生成\
自動生成されるAPIドキュメントを活用し、エンドポイントの確認や動作検証を効率化しました。
- APIテストの実装 \
fixtureを使ってテスト用データベースのセットアップを行い、各エンドポイントの正常系・異常系テストを作成しました。

## 改善点・今後の課題

- スケジュール管理 \
タスクを計画に落とし込むことはできたが、割り込みタスクや、計画が崩れたときにうまく整理していくことができませんでした。\
→タスクを行動単位に細かく分解してから粒度を合わせる\
→自分に合ったスケジュール管理フォーマットの探求

- コミットメッセージに統一感がない \
コミット履歴を見たときに何をやったのかがわかりずらい\
→コミットメッセージにルールを決めて運用する
