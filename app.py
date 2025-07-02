from flask import Flask,render_template,g
from flask import request,redirect
import sqlite3
import os

app = Flask(__name__)
DATABASE = "database.db"
@app.route("/")
def top():
    create_table()
    # insert_data()
    task_list =get_db().execute("select id,title,content,due_date,completed from tasks").fetchall()
    return render_template("index.html",task_list=task_list)


#--- タスク追加 ---
@app.route("/regist",methods=['GET','POST'])
def regist():
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
    if request.method=='POST':
        get_db().execute("delete from tasks where id=?",(id,))
        get_db().commit()
        return redirect('/')
    post =get_db().execute("select id,title,content,due_date,completed from tasks where id=?",(id,)).fetchone()
    return render_template("delete.html",post=post)
    

#--- タスク一括削除　---
@app.route("/delete_all",methods=['GET','POST'])
def delete_all():
    post_list=[]
    if request.method=='POST':
        id_list =request.form.getlist('delete_all')
        if id_list is not None:
            for id in id_list:
                post_list.append(get_db().execute("select id,title,content,due_date,completed from tasks where id=?",(id,)).fetchone())
            
    return render_template("delete_all.html",post_list=post_list)

@app.route("/deletes",methods=['GET','POST'])
def deletes():
    if request.method=='POST':
        id_list=request.form.getlist('deletes')
        for id in id_list:
            get_db().execute("delete from tasks where id=?",(id,))
        get_db().commit()
    
    return redirect('/')

#--- データベース作成、接続 ---
# instance ディレクトリがなければ作成 (このブロックも重要)
def connect_db():
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv
def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#--- テーブルの作成 ---
def create_table():
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
    
    