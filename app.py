import sqlite3
import secrets
from flask import redirect, render_template, request, session, abort
from flask import Flask
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import db
import config
import items
import users


app = Flask(__name__)
app.secret_key = config.secret_key

def check_login():
    if "user_id" not in session: 
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items = all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    return render_template("show_item.html", item=item)

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_item(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results = results)

@app.route("/new_item")
def new_item():
    check_login()
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    check_login()
    check_csrf()
    title = request.form["title"]
    description = request.form["description"]
    length = request.form["length"]
    pace = request.form["pace"]
    user_id = session["user_id"]

    items.add_item(title, length, pace, description, user_id)

    return redirect("/")

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    check_login()
    item = items.get_item(item_id)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item=item)

@app.route("/update_item", methods=["POST"])
def update_item():
    check_csrf()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if item["user_id"] != session["user_id"]:
        abort(403)
            
    title = request.form["title"]
    length = request.form["length"]
    pace = request.form["pace"]
    description = request.form["description"]

    items.update_item(item_id, title, length, pace, description)

    return redirect("/item/" + str(item_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    check_login()
    item = items.get_item(item_id)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)
    
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))

@app.route("/create", methods=["POST"])
def create():
    check_csrf()
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:      
        del session["user_id"]
        del session["username"]
    return redirect("/")