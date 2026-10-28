import os
from flask import Flask,render_template,request
import oracledb

app = Flask(__name__)
#Database Login#
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DSN = os.environ.get("DB_DSN")

try:
    with oracledb.connect(user=DB_USER,password=DB_PASSWORD,dsn = DB_DSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM cusdata")

            rows = cursor.fetchall()
            print(rows)
            print(cursor)

except Exception as e:
    print(f"Database Error{e}",flash=True)

@app.route("/")
def home():
    return render_template("input.html")

@app.route("/update")
def update():
    gmail = request.form("gmail")
    try:
        with oracledb.connect(user=DB_USER,password=DB_PASSWORD,dsn = DB_DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO cusdata (gmail) VALUES ({gmail})")
                cursor.execute("COMMIT")
                rows = cursor.fetchall()
                print(rows)
                print(cursor)
                return rows

        except Exception as e:
            print(f"Database Error{e}",flash=True)
            return "Error"
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
