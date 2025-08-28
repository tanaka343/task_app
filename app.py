from flask import Flask,render_template,g
from flask import request,redirect
import sqlite3
import os

app = Flask(__name__)
DATABASE = "database.db"

@app.route("/")
def top():
    """
    ルートページ（/）を表示
    - tasksテーブルを作成（存在しない場合のみ）
    - データベースから全タスクを取得
    - index.htmlにタスクリストを渡す
    """
    create_table()
    # insert_data()
    task_list =get_db().execute("select id,title,content,due_date,completed from tasks").fetchall()
    return render_template("index.html",task_list=task_list)


#--- タスク追加 ---
@app.route("/regist",methods=['GET','POST'])
def regist():
    """
    タスク登録ページ
    - GET: 空の登録フォーム表示
    - POST: フォームからタスク情報を取得してDBに登録
    """
    if request.method == 'POST':
        title =request.form.get('title')
        content =request.form.get('content')
        due_date =request.form.get('due_date')
        completed =request.form.get('completed')
        get_db().execute("INSERT INTO tasks (title,content,due_date,completed) values(?,?,?,?)",[title,content,due_date,completed])
        get_db().commit()
        return redirect('/')
    
    return render_template("regist.html")

#--- タスク編集 ---
@app.route("/<id>/edit",methods=['GET','POST'])
def edit(id):
    """
    タスク編集ページ

    - GET: 指定IDのタスクを取得して編集フォームを表示
    - POST: フォームから取得した値でDBを更新し、
            更新後はトップページに自動でリダイレクト
    """
    if request.method == 'POST':
        title =request.form.get('title')
        content =request.form.get('content')
        due_date =request.form.get('due_date')
        completed =int(request.form.get('completed'))
        get_db().execute("update tasks set title=?, content=?,due_date=?,completed=? where id=?",[title,content,due_date,completed,id])
        get_db().commit()
        return redirect('/')
    post =get_db().execute("select id,title,content,due_date,completed from tasks where id=?",(id,)).fetchone()
    return render_template("edit.html",post=post)

#--- タスク削除 ---
@app.route("/<id>/delete",methods=['GET','POST'])
def delete(id):
    """
    タスク削除ページ

    - GET: 指定IDのタスクを取得して確認ページ表示
    - POST: 指定IDのタスクを削除し、トップページに自動リダイレクト
    """
    if request.method=='POST':
        get_db().execute("delete from tasks where id=?",(id,))
        get_db().commit()
        return redirect('/')
    post =get_db().execute("select id,title,content,due_date,completed from tasks where id=?",(id,)).fetchone()
    return render_template("delete.html",post=post)
    

#--- タスク一括削除　---
@app.route("/delete_all",methods=['GET','POST'])
def delete_all():
    """
    タスク一括削除確認ページ

    - POST: フォームから受け取った複数のタスクIDを使ってDBからデータを取得し、
            確認ページに一覧表示する
    """
    post_list=[]
    if request.method=='POST':
        id_list =request.form.getlist('delete_all')#name='delete_allの要素のvalueをリストにして返す
        if id_list is not None:
            for id in id_list:
                post_list.append(get_db().execute("select id,title,content,due_date,completed from tasks where id=?",(id,)).fetchone())
            
    return render_template("delete_all.html",post_list=post_list)

@app.route("/deletes",methods=['GET','POST'])
def deletes():
    """
    タスク一括削除処理

    - POST: フォームから受け取った複数のタスクIDを取得し、
            ループでそれぞれのタスクをデータベースから削除。
            削除完了後はトップページにリダイレクトする。

    - GET: URLから直接アクセスの場合は、特に処理せず、トップページにリダイレクトする。
    """
    if request.method=='POST':
        id_list=request.form.getlist('deletes')
        for id in id_list:
            get_db().execute("delete from tasks where id=?",(id,))
        get_db().commit()
    
    return redirect('/')

#--- データベース作成、接続 ---
def connect_db():
    """
    SQLiteデータベースに接続する。

    - DATABASEで指定されたファイルに接続（存在しなければ新規作成）
    - row_factoryをsqlite3.Rowに設定することで、
      SQLの結果を辞書のようにカラム名でアクセス可能にする
    - 接続オブジェクトを返す
    """
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """
    現在のリクエストで使用するデータベース接続を取得する。

    - g.sqlite_dbに接続が保存されていればそれを返す
    - 保存されていなければconnect_db()で新しく接続を作成して保存
    
    """
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#--- テーブルの作成 ---
def create_table():
    """
    tasksテーブルを作成する。

    - データベースに接続（存在しなければ新規作成）
    - tasksテーブルを作成（すでに存在する場合は何もしない）
    - カラム:
        id        : タスクID（自動増分）
        title     : タスク名
        content   : 内容
        due_date  : 期限
        completed : 完了フラグ（0または1）
    - 作成後、接続を閉じる
    """
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,content TEXT,due_date TEXT,completed INTEGER)")
    con.commit()
    con.close()

#--- テストデータの挿入---
def insert_data():
    con = sqlite3.connect(DATABASE)
    title="買い物"
    content="バナナ買う"
    due_date="6/24"
    completed=1
    con.execute("INSERT INTO tasks (title,content,due_date,completed) values(?,?,?,?)",[title,content,due_date,completed])
    con.commit()
    con.close()

#--- 実行部分 ---
if __name__=="__main__":
    # with app.app_context():
    #     create_table()
    
        # insert_data()
    app.run()
    
    