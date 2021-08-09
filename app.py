from logging import error
from flask import Flask, render_template, request
from flask_pymongo import PyMongo


app = Flask("MongoDB App")
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask-mongo"

mongo_client = PyMongo(app)
mycollection = mongo_client.db.mycollection

@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/home", methods = ["GET","POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        found = mycollection.find({
            "username": username,
        })
        l = [i for i in found]
        if len(l)==0 :
            mycollection.insert_one(
                {
                    "username": username,
                    "password": password
                }
            )
            return render_template("home.html",text="Hi Newbie,",username=username)
        elif len(l)==1 and l[0]["username"]==username and l[0]["password"]==password:
            return render_template("home.html", text="Welcome Back,",username=username)
        elif len(l)==1 and l[0]["username"]==username and l[0]["password"]!=password:
            return render_template("form.html", error="Incorrect Password")


@app.route("/form2")
def form2():
    return render_template("update_username.html")

@app.route("/form3", methods=["GET","POST"])
def form3():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        new_username = request.form.get("new_username")
        found = mycollection.find({
            "username": username,
        })
        l = [i for i in found]
        if len(l)==0 :
            return render_template("update_username.html", error="Username not found!")
        elif len(l)==1 and l[0]["username"]==username and l[0]["password"]==password:
            mycollection.update_one(
                {"username": username},
                {"$set": {"username": new_username}}
            )
            return render_template("form.html", error="Username Updated")
        elif len(l)==1 and l[0]["username"]==username and l[0]["password"]!=password:
            return render_template("update_username.html", error="Incorrect Password")


@app.route("/form4")
def form4():
    return render_template("update_password.html")


@app.route("/form5", methods=["GET","POST"])
def form5():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        new_password = request.form.get("new_password")
        found = mycollection.find({
            "username": username,
        })
        l = [i for i in found]
        if len(l)==0 :
            return render_template("update_password.html", error="Username not found!")
        elif len(l)==1 and l[0]["username"]==username and l[0]["password"]==password:
            mycollection.update_one(
                {"username": username},
                {"$set": {"password": new_password}}
            )
            return render_template("form.html", error="Password Updated")
        elif len(l)==1 and l[0]["username"]==username and l[0]["password"]!=password:
            return render_template("update_password.html", error="Incorrect Password")


@app.route("/delete")
def delete():
    return render_template("delete_user.html", error="Provide the Crendentials")


@app.route("/form6", methods=["GET","POST"])
def form6():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        found = mycollection.find({
            "username": username,
        })
        l = [i for i in found]
        if len(l)==0 :
            return render_template("delete_user.html", error="Username not found!")
        elif len(l)==1 and l[0]["username"]==username and l[0]["password"]==password:
            mycollection.delete_one({
                "username": username
            })
            return render_template("form.html", error="User Deleted")
        elif len(l)==1 and l[0]["username"]==username and l[0]["password"]!=password:
            return render_template("delete_user.html", error="Incorrect Password")

app.run(host="", port=1234)