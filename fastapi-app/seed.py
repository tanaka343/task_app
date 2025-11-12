from database import SessionLocal
import csv
from models import Item
from datetime import date


db = SessionLocal()

 
with open("test_data.csv","r",encoding="utf-8") as f:
  #open('test_data.csv', 'r') = ファイルを読み込みモードで開く
  #encoding='utf-8' = 日本語対応
  #with ... as f: = 終わったら自動でファイルを閉じる
  reader = csv.DictReader(f)
  for row in reader:
    task = Item(
      title = row["title"],
      content = row["content"],
      due_date = date.fromisoformat(row["due_date"]),
      completed = row["completed"] == True
        #row['completed'] = 文字列の"True"か"False"
        #== 'True' = 文字列と比較してbool値を作る
    )
    db.add(task)

db.commit()
db.close()

print("test_tasksを挿入しました")