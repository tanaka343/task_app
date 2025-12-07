# FastAPI版 タスク管理アプリ

FastAPI と SQLAlchemy を用いて構築したタスク管理APIです。
学習目的で開発し、CRUD / 認証 / バリデーション / マイグレーション / テスト といった
バックエンド API に必要な要素を一通り実装しました。

## 目的

- Udemyで学習したFastAPIの内容をアウトプットする目的で、既存のタスク管理アプリを再構成
- FastAPI による API設計〜実装の一連の流れを習得 するため
- SQLAlchemy / Alembic を用いた データベース操作とマイグレーション管理 を学ぶため

## 機能

- タスクのCRUD操作
- 日付範囲でのタスク検索
- 今日から指定日数後までのタスク取得
- 自動生成されるAPIドキュメント（Swagger UI）
- JWT によるログイン / サインアップ
- データベースマイグレーション管理（Alembic）
- APIテスト（pytest）

## 技術スタック

FastAPI\
SQLAlchemy（ORM）\
Alembic（マイグレーション）\
SQLite\
Pydantic（バリデーション）\
python-jose（JWT 認証）\
pytest（テスト）

## ファイル構成

```python
fastapi-app/
├── cruds/      # ビジネスロジック（DB操作）
│ ├── init.py
│ ├── auth.py   # 認証関連のCRUD
│ └── task.py   # タスクCRUD
│
├── routers/    # エンドポイント定義
│ ├── init.py
│ ├── auth.py   # /login など認証系
│ └── task.py   # /tasks API
│
├── migrations/ # Alembic マイグレーションファイル
│
├── tests/      # pytest テスト
│ ├── conftest.py # テスト用DBなどのfixture
│ └── test_main.py # エンドポイントのテスト
│
├── alembic.ini # Alembic 設定
├── database.py # DB 接続・セッション管理
├── main.py     # FastAPI エントリポイント
├── models.py   # SQLAlchemy モデル
├── schemas.py  # Pydantic スキーマ
├── seed.py     # オプションデータ投入スクリプト
├── test_data.csv # オプションデータ
└── README.md   # FastAPI版 README
```

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r ../requirements.txt

```

### 2. データベースのセットアップ

```bash
#マイグレーション実行（テーブル作成）
alembic upgrade head
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
  "user_id": 1
}
```

### エンドポイント一覧

| メソッド | エンドポイント        | 説明                                        | パラメータ                          | 認証 |
|---------|----------------------|---------------------------------------------|--------------------------------------|------|
| POST    | `/login`             | ログインして JWT を取得                    　 | -                                    | 不要 |
| POST    | `/signup`            | ユーザー登録                              　 | -                                    | 不要 |
| GET     | `/tasks`             | 全タスク取得                                 | -                                    | 必要 |
| GET     | `/tasks/{id}`        | ID 指定タスク取得                            | -                                    | 必要 |
| POST    | `/tasks`             | タスク作成                                   | JSON ボディ                          | 必要 |
| PUT     | `/tasks/{id}`        | タスク更新                                   | JSON ボディ                         　| 必要 |
| DELETE  | `/tasks/{id}`        | タスク削除                                   | -                                   | 必要 |
| GET     | `/tasks/`            | 指定した期限日、または期限日からn日後まで取得   | `due_date`（必須）, `end`（任意）    | 不要 |
| GET     | `/today`             | 今日から n日後までのタスク取得              　 | `end`（任意）                      | 不要 |

## 工夫した点・学んだこと

### API機能の工夫

- ユーザービリティを考えて今日（開始日）から何日後までのタスクを取得できるようにした。

### 技術的なこと

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
