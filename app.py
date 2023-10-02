from flask import Flask, render_template, request, session, redirect, url_for
from flask_migrate import migrate, Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = b'8dca3728bc7f6f5dd69074176ca0addf02e0290bec9840783e35f347a56d52e3'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
class Cart(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(30), nullable=False)
    user_name = db.Column(db.String(30), nullable=False)
    count = db.Column(db.Integer, default=0)

    def __str__(self):
        return f'{self.count} {self.item_name}(s)'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(30), nullable=False)
    




@app.route("/")
def index():
    
    if not session.get("name"):
        return render_template("login.html")

    return render_template("index.html", name=session.get("name"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if not request.form.get("name", "").strip():
        return redirect(url_for("index"))
    session["name"] = request.form.get("name").title().strip()

    return redirect(url_for("index"))


@app.route("/logout")
def logout():

    session["name"] = None

    return redirect(url_for("index"))


@app.route("/addcart", methods=["GET", "POST"])
def add_cart():
    item_name = request.form.get("name")
    user_name = session.get("name")
    if not user_name:
        return redirect(url_for("logout"))
    if not item_name:
        return redirect(url_for("index"))
    item = Cart.query.filter_by(item_name=item_name, user_name=user_name).first()
    if item:
        item.count += 1
        db.session.commit()
        return redirect(url_for("index"))
    
    item = Cart(item_name=request.form.get("name"), user_name=user_name, count=1)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/showcart")
def show_cart():
    user_name = session.get("name")
    if not user_name:
        redirect(url_for("index"))
    cart_items = Cart.query.filter_by(user_name=session.get("name")).all()
    return render_template("show_cart.html", cart_items=cart_items, user_name=user_name)
