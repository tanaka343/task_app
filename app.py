from flask import Flask,render_template,g
import sqlite3
DATABASE = "database.db"
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


    
#--- データベース作成、接続 ---
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
    con.execute("CREATE TABLE IF NOT EXISTS memo(id integer primary key autoincrement,title text,content text,due_date text,completed integer)")


#--- 実行部分 ---
if __name__=="__main__":
    create_table()
    app.run()