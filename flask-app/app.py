from flask import Flask,render_template,g,session,url_for
from flask import request,redirect
import sqlite3
import os
import requests

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)),"database.db")

@app.route("/")
def top():
    """
    ルートページ（/）を表示
    - tasksテーブルを作成（存在しない場合のみ）
    - データベースから全タスクを取得
    - index.htmlにタスクリストを渡す
    """
    create_table()
    
    task_list =get_db().execute("select id,title,content,due_date,completed from tasks").fetchall()
    return render_template("index.html",task_list=task_list)

#---ログイン画面---
FASTAPI_URL = 'http://localhost:8000'  # FastAPIのURL
app.secret_key = "8db6474b23b4eef4b0f9318a706cd4014323acf10991f5d5194a6bcb92e896d3"
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(f"Username: {username}")  
        print(f"Password: {password}")
    
        response = requests.post(
            f'{FASTAPI_URL}/auth/login',# fastapiのauthエンドポイントにprefixがついているため
            data={'username': username, 'password': password}
        )
        print(f"Status Code: {response.status_code}")  
        print(f"Response Body: {response.text}")  
        
        if response.status_code==200:
            token = response.json()['access_token']
            session['jwt_token'] = token
            return redirect(url_for("login_sc"))
        else:
            return render_template("login.html",error='ログイン失敗')
    return render_template("login.html")

@app.route("/task_list")
def login_sc():
    return "login successful"



#--- タスク追加 ---
@app.route("/regist",methods=['GET','POST'])
def regist():
    """
    タスク登録ページ
    - GET: 空の登録フォーム表示
    - POST: フォームからタスク情報を取得してDBに登録
            更新後はトップページに自動でリダイレクト
    """
    #POSTの場合、フォームから情報を取得してDBに登録
    if request.method == 'POST':
        title =request.form.get('title')
        content =request.form.get('content')
        due_date =request.form.get('due_date')
        completed =request.form.get('completed')
        get_db().execute("INSERT INTO tasks (title,content,due_date,completed) values(?,?,?,?)",[title,content,due_date,completed])
        get_db().commit()
        return redirect('/')
    #GETの場合そのまま返す
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
    #POSTの場合、フォームから情報を取得してDBに登録
    if request.method == 'POST':
        title =request.form.get('title')
        content =request.form.get('content')
        due_date =request.form.get('due_date')
        completed =int(request.form.get('completed'))
        get_db().execute("update tasks set title=?, content=?,due_date=?,completed=? where id=?",[title,content,due_date,completed,id])
        get_db().commit()
        return redirect('/')
    #GETの場合、idを指定してDBから情報を取得し、編集フォームへ表示
    task =get_db().execute("select id,title,content,due_date,completed from tasks where id=?",(id,)).fetchone()
    return render_template("edit.html",task=task)

#--- タスク削除 ---
@app.route("/<id>/delete",methods=['GET','POST'])
def delete(id):
    """
    タスク削除ページ

    - GET: 指定IDのタスクを取得して確認画面表示
    - POST: 指定IDのタスクを削除し、トップページに自動リダイレクト
    """
    #POSTの場合idを指定してDBからデータ削除
    if request.method=='POST':
        get_db().execute("delete from tasks where id=?",(id,))
        get_db().commit()
        return redirect('/')
    
    #GETの場合、idを指定してDBから情報を取得し、確認画面表示
    task =get_db().execute("select id,title,content,due_date,completed from tasks where id=?",(id,)).fetchone()
    return render_template("delete.html",task=task)
    

#--- タスク一括削除　---
@app.route("/delete_all",methods=['GET','POST'])
def delete_all():
    """
    タスク一括削除確認ページ

    - GET: task_list=[]の場合のHTMLを表示
    - POST: TOPのフォームから受け取った複数のタスクIDを使ってDBからデータを取得し、
            確認ページに一覧表示する
            ※複数IDをBodyに入れて送るためPOST
    """
    #POSTの場合、フォームから複数IDを取得しBodyに情報を入れて送信、DBから情報を取得し、確認ページを表示
    task_list=[]
    if request.method=='POST':
        id_list =request.form.getlist('delete_all')#name='delete_allの要素のvalueをリストにして返す
        if id_list is not None:
            for id in id_list:
                task_list.append(get_db().execute("select id,title,content,due_date,completed from tasks where id=?",(id,)).fetchone())

    #GETの場合、task_list=[]の場合のHTMLを表示        
    return render_template("delete_all.html",task_list=task_list)

@app.route("/deletes",methods=['GET','POST'])
def deletes():
    """
    タスク一括削除処理

    - POST: タスク一括削除確認ページのフォームから複数のタスクIDを取得し、
            ループでそれぞれのタスクをデータベースから削除。
            削除完了後はトップページにリダイレクトする。

    - GET: URLから直接アクセスの場合は、特に処理せず、トップページにリダイレクトする。
    """
    #POSTの場合、フォームから複数のIDを取得しDBから削除
    if request.method=='POST':
        id_list=request.form.getlist('deletes')
        for id in id_list:
            get_db().execute("delete from tasks where id=?",(id,))
        get_db().commit()
    
    #GETの場合、TOPページを表示
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


#--- 実行部分 ---
if __name__=="__main__":
        
    app.run()
    
    