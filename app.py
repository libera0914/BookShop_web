from flask import Flask
from flask import render_template
from flask import request
from flask import session
from make_db import *
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = 'please-generate-a-random-secret_key'


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login', methods=['GET','POST'])
def index():
    if request.method == "POST": 
        session['username'] = request.form['user']
        session['password'] = request.form['password']
        conn = sqlite3.connect('products.db')
        c = conn.cursor() 
        sql ="select flag from users where username='{}' and password ='{}'".format(session['username'],session['password'])
        c.execute(sql)
        res = c.fetchall()
        c.close()
        if res:
            if res[0][0]  == '1':
                res = all_book() 
                return render_template("admin.html", name=session['username'], res=res)
            elif res[0][0] == "2":
                res = all_book()
                init_record(session['username'])
                return render_template("customer.html", name=session['username'], res=res)
            else:
                return "password error"
        else:
            return render_template("login.html", result="error")
    else:
        conn = sqlite3.connect('products.db')
        c = conn.cursor()#
        sql = """select flag from users where username='{}' and password ='{}'""".format(session['username'],session['password'])
        c.execute(sql)
        res = c.fetchall()
        c.close()
        if res:
            if res[0][0]   == '1':
                res = all_book()
                return render_template("admin.html", name=session['username'], res=res)
            elif res[0][0] == "2" :
                res = all_book()
                return render_template("customer.html", name=session['username'], res=res)
            else:
                return "password error"


@app.route('/add', methods=['GET','POST'])
def add(): 
    if request.method == "POST": 
        conttent = [] 
        f = request.files['file'] 
        path = "./static/file/{}".format(f.filename)
        f.save(path)#Save file picture
        for k,v in  request.form.to_dict().items(): 
            conttent.append(v)  
        conttent.append(path)  
        add_book(conttent) 
        return render_template("success.html") 

@app.route('/upload', methods=['GET','POST']) 
def upload(): 
    if request.method == "POST": 
        f = request.files['file']
        f.save("./static/file".strip()) 
       
@app.route('/record', methods=['GET','POST']) 
def record(): 
    if request.method == "POST": 
        res = int(request.data) 
        add_record(session['username'],res) 

@app.route('/car', methods=['GET','POST']) 
def car():
    list_num = select_id(session['username']) 
    res = select_show(session['username'],list_num) 
    if len(res) == 0: 
        a=0
    else:
        a = res[-1][4] 

    return render_template("shopping.html", res=res,a=a)

@app.route('/delcar', methods=['GET','POST']) 
def delcar():
    id =int(request.data) 
    del_car(session['username'],id) 

@app.route('/delcount', methods=['GET','POST']) 
def delcount():
    id =int(request.data)  
    changecount("del",session['username'],id) 
    return "a"

@app.route('/addcount', methods=['GET','POST'])
def addcount():
    id = int(request.data)
    changecount("add",session['username'],id)
    return "a"

@app.route('/clear', methods=['GET','POST']) 
def clear():
    clearcar(session['username']) 
    return "a"

@app.route('/apply', methods=['GET','POST'])
def apply():
    list_num = select_id(session['username'])
    res = select_show(session['username'], list_num)
    # print(res[-1][4])
    info = ""
    fare = 3

    all_list = []
    #print(res)
    for i in res:
        tmp_list = []
        info = info + i[1][0]+","
        tmp_list.append(i[1][0])
        tmp_list.append(i[2])
        #print(tmp_list)
        all_list.append(tmp_list)

    if len(res) == 0:
        a = 0
    else:
        a = res[-1][4]
    fare = (res[-1][5] -1 )*1 +fare
    session['list'] = all_list
    return render_template("apply.html",info=info,a=a,fare=fare)

@app.route('/success', methods=['GET','POST'])

def success():
    print(session['list'])
    res = select_book_count(session['list'])
    if res:
        return render_template("suc.html",a="success")
    else:
        return render_template("suc.html", a="fail")

@app.route('/addadmin', methods=['GET','POST']) 
def addadmin(): 
    return render_template("add.html") 

if __name__ == '__main__':
    app.run(debug=True, port="5000")
