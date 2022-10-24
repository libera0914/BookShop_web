import sqlite3


def init_db():#Create a database table
    con = sqlite3.connect('products.db')
    con.execute(
        'CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(255), password VARCHAR(255),flag  VARCHAR(255))')
    
    con.execute(
        'CREATE TABLE books(id INTEGER PRIMARY KEY AUTOINCREMENT, bookname VARCHAR(255), author VARCHAR(255),creattime  VARCHAR(255),isbn  VARCHAR(255),detail  VARCHAR(255),saleprice  INT unsigned,rprice INT unsigned,bookcount INT unsigned,images VARCHAR(255))'
    )
    
    con.execute(
        'CREATE TABLE record(id INTEGER PRIMARY KEY, username VARCHAR(255), nums VARCHAR(255))'
    )
    
    
    con.close()
    
    con = sqlite3.connect('products.db')
    con.execute(
        'INSERT INTO users(id, username, password,flag) VALUES (1, "admin", "p455w0rd",1),(2, "customer1", "p455w0rd",2),(3, "customer2", "p455w0rd",2);')
    
    con.commit()
    con.close()

def all_book():
    con = sqlite3.connect('products.db')
    sql = "select bookname,isbn,images,id,saleprice from books " 
    res = con.execute(sql).fetchall()
    code_list = list_of_groups(res,5)
    con.close()
    return code_list



def add_book(content): 
    con = sqlite3.connect('products.db') 
    sql = "insert into books values(null,'{}','{}','{}','{}','{}',{},{},{},'{}')".format(content[0],content[1],content[2],content[3],content[4],content[5],content[6],content[7],content[8]) 
    print(sql)
    con.execute(sql) 
    con.commit() 
    con.close() 

def list_of_groups(init_list, children_list_len):
    list_of_groups = zip(*(iter(init_list),) * children_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % children_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list

def init_record(user):
    con = sqlite3.connect('products.db')
    sql = "delete  from record where username='{}'".format(user)
    con.execute(sql)
    con.commit()
    con.close()

def add_record(user,id): 
    con = sqlite3.connect('products.db') 
    sql = "select *  from record where username='{}' and nums = {}".format(user,id) 
    res = con.execute(sql).fetchall() 
    if res: #The record has been recorded and deleted
        sql = "delete  from record where username='{}' and nums = {}".format(user,id) 
        con.execute(sql) 
        con.commit()
    else: 
        sql = "insert into record values({},'{}',1)".format(id,user) 
        con.execute(sql)
        con.commit()

    con.close()

def select_id(user):
    con = sqlite3.connect('products.db')
    sql = "select DISTINCT(id),nums from record where username='{}'".format(user)
    res = con.execute(sql).fetchall()
    list_num = {}
    for i in res:
        list_num[i[0]]=i[1]
    con.close()
    return list_num

def select_show(user,list_num):
    all_m = 0
    book_count = 0
    count=1
    con = sqlite3.connect('products.db')
    list_show = []
    for k,v in list_num.items():
        sql = "select bookname,images,saleprice from books where id='{}'".format(k)
        #print(sql)
        res = con.execute(sql).fetchall()
        res.insert(0,count)
        count +=1
        res.append(v)
        #print(res)
        all_m = all_m +int(v) * int(res[1][2])
        book_count = book_count+int(v)
        res.append(k)
        res.append(all_m)
        res.append(book_count)
        list_show.append(res)
    con.close()
    print(list_show)
    return list_show

def del_car(user,id):
    con = sqlite3.connect('products.db')
    sql = "delete from record where username = '{}' and id='{}'".format(user,id)
    con.execute(sql)
    con.commit()
    con.close()

def changecount(flag,user,id):
    con = sqlite3.connect('products.db')
    sql = "select nums from record where username = '{}' and id='{}'".format(user, id) 
    res = con.execute(sql).fetchall() 
    if flag == "add": 
        num = int(res[0][0]) + 1
    else: 
        num = int(res[0][0]) - 1
        if num < 0: 
            num = 0
    sql = "update record set nums = {}  where username = '{}' and id='{}'".format(num,user, id) 
    con.execute(sql)
    con.commit()
    con.close() 


def clearcar(user):
    con = sqlite3.connect('products.db') 
    sql = "delete from record where username = '{}'".format(user) 
    con.execute(sql) 
    con.commit()
    con.close()
    
def select_book_count(books):
    flag = 1
    sql_list = []
    for book in books:
        con = sqlite3.connect('./products.db')

        sql = "select bookcount from books where bookname = '{}'".format(book[0])
        print(sql)
        res = con.execute(sql).fetchall()
        count = res[0][0]
        print(count)
        if int(count) >= int(book[1]):
            flag =1
            num =  int(count) - int(book[1])
            sql ="update books set bookcount ={} where bookname = '{}'".format(num ,book[0])
            sql_list.append(sql)
        else:
            flag =0
            return  False
    con.close()
    for sql in sql_list:
        con = sqlite3.connect('./products.db')
        con.execute(sql)
        con.commit()
        con.close()
    return  True


if __name__ == '__main__':
    #all_book()

    #init_db()
    books =[['looklook', '1'],['looklook1', '1']]
    list_num = select_book_count(books=books)
    print(list_num)
    conttent = ['test1', 'a', '20211116', '1', '1', 1, 1, 1, '1']

