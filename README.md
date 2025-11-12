# タスク管理アプリ

FlaskとFastAPIを使ったタスク管理アプリケーションの学習プロジェクトです。
同じ機能を2つの異なるフレームワークで実装することで、それぞれの特徴や違いを学ぶことを目的としています。

## ディレクトリツリー

```python
.
├── README.md           # このファイル
├── flask-app/          # Flask実装
└── fastapi-app/        # FastAPI実装
```

## 各実装の特徴

### Flask版 (flask-app/)

- フロントエンド付き - HTMLテンプレートを使用したWebインターフェース\
- 一括削除機能 - 複数のタスクをまとめて削除可能\
- シンプルで学習しやすい構造\
- 詳細は [flask-app/README.md](./flask-app/README.md) を参照

### FastAPI版 (fastapi-app/)

- 日付フィルタリング - 指定した日数後までのタスクを取得可能
- SQLAlchemy - ORMを使ったデータベース操作
- Alembic - データベースマイグレーション管理
- 自動生成されるAPIドキュメント（Swagger UI）
- 詳細は [fastapi-app/README.md](./fastapi-app/README.md)を参照

## 主な機能

両方の実装で以下の基本機能を提供：

タスクの作成（Create）\
タスクの取得（Read）\
タスクの更新（Update）\
タスクの削除（Delete）

## 技術スタック

バックエンド: Flask / FastAPI\
フロントエンド（Flask版のみ）: HTML, CSS\
データベース: SQLite\
ORM (FastAPI版のみ) : SQLAlchemy\
マイグレーション (FastAPI版のみ) : Alembic\
言語: Python

## 開発目的

このプロジェクトは学習目的で作成しました。FlaskとFastAPIの以下の点を比較・学習できます：

ルーティングの書き方\
リクエスト/レスポンスの処理\
エラーハンドリング\
データベース操作（直接SQL vs ORM）\
データベースマイグレーション管理（Alembic）\
APIドキュメント自動生成（FastAPI）

## 詳細情報

各実装の詳しいセットアップ方法や使い方は、それぞれのREADMEを参照してください：

- [Flask版のREADME](./flask-app/README.md)
- [FastAPI版のREADME](./fastapi-app/README.md)
