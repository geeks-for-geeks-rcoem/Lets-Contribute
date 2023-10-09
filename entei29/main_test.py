from functools import wraps
from flask import Flask, request
from flask import Flask, render_template, request, redirect, url_for, flash, session

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# ********************** Config ***********************
app.config['SECRET_KEY'] = "local_secret_key_12345"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///grocery.sqlite3'
db = SQLAlchemy(app)

# ********************** Models ***********************


class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, nullable=False,
                        primary_key=True, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    passhash = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    @property
    # getter
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    # setter
    def password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passhash, password)


class Orders(db.Model):
    __tablename__ = "orders"
    order_id = db.Column(db.Integer, nullable=False,
                         primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String, nullable=False)
    total = db.Column(db.Float, nullable=False)


class Units(db.Model):
    __tablename__ = "units"
    u_id = db.Column(db.Integer, nullable=False,
                     primary_key=True, autoincrement=True)
    u_name = db.Column(db.String, nullable=False)


class Products(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, nullable=False,
                           primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey(
        "units.u_id"), nullable=False, default=1)
    price_per_unit = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        "categories.category_id"), nullable=False)


class Order_details(db.Model):
    __tablename__ = "order_details"
    order_id = db.Column(db.Integer, db.ForeignKey(
        "orders.order_id"), nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "products.product_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)


class Categories(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, nullable=False,
                            primary_key=True, autoincrement=True)
    category_name = db.Column(db.String, nullable=False, unique=True)
    products = db.relationship("Products", backref="categories", lazy=True)

# to create database if it doesn't exist


with app.app_context():
    db.create_all()
    admin = Users.query.filter_by(is_admin=True).first()
    if not admin:
        admin = Users(username="admin", password="admin",
                      name="admin", is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("Admin account created.")


# ********************** Routes ***********************

# decorator is a function that takes another function as an argument
def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if "user_id" not in session:
            flash("Error: please login first.")
            return (redirect(url_for("user_login")))
        return func(*args, **kwargs)
    return inner


def admin_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if "user_id" not in session:
            flash("Error: please login first.")
            return (redirect(url_for("user_login")))
        user = Users.query.filter_by(user_id=session["user_id"]).first()
        if not user.is_admin:
            flash("Error: you are not authorised to access this page.")
            return (redirect(url_for("user_login")))
        return func(*args, **kwargs)
    return inner


@app.route("/", methods=["GET", "POST"])
def user_login():
    if request.method == "GET":
        return render_template("user_login.html")
    elif request.method == "POST":
        # request.args is for "get" request
        # request.form is for "post" request
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "" or password == "":
            flash("Error: username or password cannot be empty.")
            return (redirect(url_for("user_login")))
        user = Users().query.filter_by(username=username).first()
        if (not user):
            flash("Error: user does not exist.")
            return (redirect(url_for("user_login")))
        if (not user.check_password(password)):
            flash("Error: incorrect password.")
            return (redirect(url_for("user_login")))
        # login succesful
        session["user_id"] = user.user_id
        return (redirect(url_for("user_dashboard")))


@app.route("/registeration", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")

        if username == "" or password == "":
            flash("Error: username or password cannot be empty.")
            return (redirect(url_for("register")))

        if Users().query.filter_by(username=username).first():
            flash("Error: username already exists, please choose another one.")
            return (redirect(url_for("register")))

        user = Users(username=username, password=password, name=name)
        db.session.add(user)
        db.session.commit()
        flash("User registration successful.")
        return (redirect(url_for("user_login")))


@app.route("/user_dashboard")
@auth_required
def user_dashboard():
    user = Users.query.filter_by(user_id=session["user_id"]).first()
    if user.is_admin:
        return (redirect(url_for("admin_dashboard")))
    else:
        return render_template("user_dashboard.html", user=user)


@app.route("/user_cart")
@auth_required
def user_cart():
    user = Users.query.filter_by(user_id=session["user_id"]).first()
    return render_template("user_cart.html", user=user)


@app.route("/admin_dashboard")
@admin_required
def admin_dashboard():
    user = Users.query.filter_by(user_id=session["user_id"]).first()
    if not user.is_admin:
        flash("Error: you are not authorised to access this page.")
        return (redirect(url_for("user_login")))
    return render_template("admin_dashboard.html", user=user, categories=Categories.query.all())


@app.route("/logout")
@auth_required
def logout():
    session.pop("user_id", None)
    return (redirect(url_for("user_login")))


@app.route("/orders")
@auth_required
def orders():
    return ""

# *****************Categories**********************


@app.route("/category/add", methods=["GET", "POST"])
@admin_required
def add_category():
    user = Users.query.filter_by(user_id=session["user_id"]).first()
    if request.method == "GET":
        return render_template("category/add.html", user=user)
    elif request.method == "POST":
        name = request.form.get("name")
        if name == "":
            flash("Error: category name cannot be empty.")
            return (redirect(url_for("add_category")))
        if len(name) > 64:
            flash("Error: category name cannot be longer than 64 characters.")
            return (redirect(url_for("add_category")))
        category = Categories(category_name=name)
        db.session.add(category)
        db.session.commit()
        flash("Category added successfully.")
        return (redirect(url_for("admin_dashboard")))


@app.route("/category/<int:category_id>/show")
@admin_required
def show_category(category_id):
    user = Users.query.filter_by(user_id=session["user_id"]).first()
    category = Categories.query.get(category_id)
    return (render_template("category/show.html", user=user, category=category))


@app.route("/category/<int:category_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_category(category_id):
    if request.method == "GET":
        user = Users.query.filter_by(user_id=session["user_id"]).first()
        return render_template("category/edit.html", user=user)
    elif request.method == "POST":
        category = Categories.query.filter_by(category_id=category_id).first()
        name = request.form.get("name")
        if name == "":
            flash("Error: category name cannot be empty.")
            return (redirect(url_for("edit_category")))
        if len(name) > 64:
            flash("Error: category name cannot be longer than 64 characters.")
            return (redirect(url_for("edit_category")))
        category.category_name = name
        db.session.commit()
        flash("Category edited successfully.")
        return (redirect(url_for("admin_dashboard")))


@app.route("/category/<int:category_id>/delete", methods=["GET"])
@admin_required
def delete_category(category_id):
    category = Categories.query.filter_by(category_id=category_id).first()
    if not category:
        flash("Error: category does not exist.")
        return (redirect(url_for("admin_dashboard")))
    db.session.delete(category)
    db.session.commit()
    flash("Category deleted successfully.")
    return (redirect(url_for("admin_dashboard")))

# *****************Products**********************


@app.route("/product/add", methods=["GET", "POST"])
@admin_required
def add_product():
    if request.method == "GET":
        cat_id = -1
        args = request.args
        if "cat_id" in args:
            if db.session.get(Categories, int(args.get('cat_id'))):
                cat_id = int(args.get('cat_id'))

        user = Users.query.get(session["user_id"])
        categories = Categories.query.all()
        return (render_template("products/add.html",
                                user=user,
                                cat_id=cat_id,
                                categories=categories))

    elif request.method == "POST":

        name = request.form.get("name")
        price_per_unit = request.form.get("price_per_unit")
        quantity = request.form.get("quantity")
        category = request.form.get("category")

        if name == "" or price_per_unit == "" or quantity == "" or category == "":
            flash("Error: All the fields are required.")
            return (redirect(url_for("add_product", category=category)))
        if quantity.isdigit() == False:
            flash("Error: quantity must be a number.")
            return (redirect(url_for("add_product", category=category)))
        quantity = int(quantity)
        if price_per_unit.isdigit() == False:
            flash("Error: price_per_unit must be a number.")
            return (redirect(url_for("add_product", category=category)))
        price_per_unit = int(price_per_unit)
        category = Categories.query.get(category)

        if not category:
            flash("Error: category does not exist.")
            return (redirect(url_for("add_product", category=category)))
        pro_name = Products(name=name, price_per_unit=price_per_unit,
                            category=category, quantity=quantity)
        db.session.add(pro_name)
        db.session.commit()
        flash("Product added successfully.")
        return (redirect(url_for("show_category", category_id=category.category_id)))


@app.route("/product/<int:product_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    pass


@app.route("/product/<int:product_id>/delete", methods=["GET", "POST"])
@admin_required
def delete_product(product_id):
    if request.method == "GET":
        user = Users.query.filter_by(user_id=session["user_id"]).first()
        product = Products.query.get(product_id)

        if not product:
            flash("Error: product does not exist.")
            return (redirect(url_for("admin_dashboard")))
        return (render_template("products/delete.html", user=user, product=product))
    elif request.method == "POST":
        product = Products.query.get(product_id)
        if not product:
            flash("Error: product does not exist.")
            return (redirect(url_for("admin_dashboard")))
        db.session.delete(product)
        db.session.commit()
        flash("Product deleted successfully.")
        return (redirect(url_for("admin_dashboard")))


# ********************** Main ***********************


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
