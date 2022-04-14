from flask import Flask, render_template, request, session
import sqlite3 as sql
from werkzeug.utils import redirect

connection = sql.connect("user1.db", check_same_thread=False)
table = connection.execute("select name from sqlite_master where type='table' AND name='user1'").fetchall()
if table != []:
     print("Table already exist")
else:
    connection.execute('''create table user1(
                                ID integer primary key autoincrement,
                                name text,
                                phone_number integer,
                                email integer,
                                password integer

                                )''')

    print("Table Created Successfully!")


Grocery = Flask(__name__)

@Grocery.route("/")
def home():
    return render_template("index.html")

@Grocery.route("/register",methods = ["GET","POST"])
def new_user():
    if request.method == "POST":
        getname = request.form["name"]
        getphone_number = request.form["phone_number"]
        getemail = request.form["email"]
        getpassword = request.form["password"]
        print(getname)
        print(getphone_number)
        print(getemail)
        print(getpassword)

        try:
            connection.execute("insert into user1(name,phone_number,email,password)\
                               values('" + getname + "'," + getphone_number + ",'" + getemail + "'," + getpassword + ")")
            connection.commit()
            print("User1 Data Added Successfully!")

        except Exception as e:
            print("Error occured ", e)



    return render_template("register.html")

@Grocery.route("/userlogin", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        getEmail = request.form["email"]
        getPass = request.form["password"]
        cursor = connection.cursor()
        query = ("select * from user1 where email='" + getEmail + "' and password='" + getPass + "'")
        result = cursor.execute(query).fetchall()
        if len(result) > 0:
            for i in result:
                getName = i[1]
                getId = i[0]
                session["name"] = getName
                session["id"] = getId
                if (getEmail == i[3] and getPass == i[5]):
                    print("password correct")
                    return redirect('/userdashboard')
                else:
                    return render_template("userlogin.html", status=True)
        else:
            return render_template("index.html", status=False)

    return render_template("userlogin.html")

@Grocery.route('/products')
def products():
    return render_template("products.html")

if __name__ == "__main__":
    Grocery.run(debug=True)