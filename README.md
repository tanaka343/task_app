# タスク管理アプリ

Flask と FastAPI を使って同じ機能を実装し、\
フロントエンドと API サーバーを分離する構成を学ぶプロジェクトです。\
最終的に 画面（Flask） と 業務ロジック（FastAPI） を分離し、連携させています。

## 開発ステップ
<!-- ## 各アプリの特徴

### Flask版 (flask-app/)
- フロントエンド - HTMLテンプレートを使用したWebインターフェース\
- 一括削除機能 - 複数のタスクをまとめて削除可能\
- 詳細は [flask-app/README.md](./flask-app/README.md) を参照

### FastAPI版 (fastapi-app/)
- 日付フィルタリング - 指定した日数後までのタスクを取得可能
- SQLAlchemy - ORMを使ったデータベース操作
- Alembic - データベースマイグレーション管理
- 自動生成されるAPIドキュメント（Swagger UI）
- JWT認証
- 詳細は [fastapi-app/README.md](./fastapi-app/README.md)を参照 -->

### 1. Flask 版の開発（初期版：Webアプリとして実装）

最初のステップでは、まず動くアプリを作ること を目的に Flask で実装しました。

- HTMLテンプレートを用いた Web UI の構築
- タスク CRUD 機能
- 一括削除機能
- 画面操作中心のシンプルな構成

- 詳細は [flask-app/README.md](./flask-app/README.md) を参照

### 2. FastAPI 版の開発

次のステップでは、バックエンドを API に分離した構成を理解・実装すること を目的に FastAPI 化しました。

- 日付フィルタリング - 指定した日数後までのタスクを取得可能
- SQLAlchemy - ORMを使ったデータベース操作
- Alembic - データベースマイグレーション管理
- 自動生成されるAPIドキュメント（Swagger UI）
- pytest による API テスト

- 詳細は [fastapi-app/README.md](./fastapi-app/README.md)を参照

### 3. JWT 認証 + Flask から FastAPI を呼び出す構成（最終ステップ）

最後のステップでは、アプリをより実務的な構成にするため、
フロント（Flask） → API（FastAPI） への完全分離を行い、
JWT 認証を実装して安全な API 利用 ができるようにしました。

- FastAPI で JWT の発行・検証を実装
- Flask が FastAPI の /login にログイン情報を送信
- JWT を保持したうえで API を利用（Bearer 認証）
- 画面と API の完全分離構造を構築
- 実務に近い「フロント → API サーバー」モデルを再現
- 詳細は「JWT認証」「Flask × FastAPI連携」セクションを参照

## ディレクトリツリー

```python
task_app
├── README.md           # このファイル
├── flask-app/          # Flask実装
└── fastapi-app/        # FastAPI実装
```

## 各サービスの役割

### Flask版 （フロント兼軽いバックエンド）

- 画面表示
- ユーザー操作
- JWT を使ってFastAPIと通信


### FastAPI版 （APIサーバー）

- 認証（JWT）
- DB操作
- タスクのCRUD

## JWT 認証
このプロジェクトでは、ユーザー認証に JWT（JSON Web Token） を使用しています。
JWT を使うことで、API 間で安全にユーザー情報を受け渡すことができます。

### 認証フロー概要

- ユーザーがユーザー名とパスワードでログイン
- FastAPI がパスワードを検証し、JWT を発行
- クライアント（Flask）が JWT を Authorization: Bearer <token> として送信
- FastAPI が JWT を検証し、ユーザーだけが利用できるAPIを実行

### なぜ JWT を採用したか

- セッション管理が不要
- API（FastAPI）とフロント（Flask）の分離と相性が良い
- トークンをヘッダに載せるだけで認証が可能

### 使用している主な技術

- hashlib.pbkdf2_hmac：パスワードハッシュ化
- os.urandom：ソルト生成
- python-jose：JWT の発行・検証
- OAuth2PasswordBearer：FastAPI 標準の認証仕組み

## Flask × FastAPI の連携
このプロジェクトでは、フロントエンド（Flask） と API サーバー（FastAPI） を分離して構築しています。\
Flask は画面表示とユーザー入力を担当し、実際のデータ処理は FastAPI 側が行う構造になっています。

### 連携の流れ

1. Flask でユーザーがログイン情報を送信
2. Flask が FastAPI の /login API にリクエストを送る
3. FastAPI が認証を行い、JWT を発行
4. Flask は受け取った JWT をブラウザ内に保持
5. 以降の操作（タスク取得・作成・更新・削除）は
JWT をヘッダーに付けて FastAPI の API を呼び出す

### なぜこの構成にしたか

- フロント（Flask）とバックエンド（FastAPI）の役割が明確
- API と画面が分離され、実践的な Web サービス構成を学べる
- 将来的にフロントを別技術（React 等）へ差し替えやすい

### 利用しているエンドポイント例（FastAPI側）

- POST /login : JWT 発行
- GET /tasks : JWT を使ったタスク一覧取得
- POST /tasks : タスク作成
- PUT /tasks/{id} : タスク更新
- DELETE /tasks/{id} : タスク削除

Flask はこれらの API を内部でコールし、画面に結果を表示します。

## 技術スタック

バックエンド: Flask / FastAPI\
フロントエンド（Flask版のみ）: HTML, CSS\
データベース: SQLite\
ORM (FastAPI版のみ) : SQLAlchemy\
マイグレーション (FastAPI版のみ) : Alembic\
認証: JWT\
言語: Python
## セットアップ方法

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```
### 2. FastAPIのセットアップ
```bash
#マイグレーション実行（テーブル作成）
cd fastapi-app
alembic upgrade head
uvicorn main:app --reload
```
起動後：
FastAPI ドキュメント → http://127.0.0.1:8000/docs

### 3. Flask のセットアップ（フロント）
```bash
cd flask-app
flask run
```

起動後：
Flask 画面 → http://127.0.0.1:5000

### 使用方法

1. Flask のログイン画面からログイン
2. Flask が FastAPI の /login にリクエストを送り JWT を取得
3. 以降、Flask 画面からタスクを操作すると FastAPI API が動く

<!-- ## シーケンス図 or 全体アーキテクチャ図 -->

## 今後の改善予定
- 今日のタスク、今日から何日後のタスクエンドポイントをフロントエンドに実装
- loggingでのログ出力
- api同士の連携

## 詳細情報

- [Flask版のREADME](./flask-app/README.md)
- [FastAPI版のREADME](./fastapi-app/README.md)
