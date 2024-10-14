from flask import Flask, render_template, request, session, redirect, url_for
import random
from flask_sqlalchemy import SQLAlchemy
import uuid
import os
from dotenv import load_dotenv



load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')

# Creates an SQLAlchemy instance
db = SQLAlchemy(app)



# List of messages
messagesList = ["Hello! My name is ChatBot, please type your query below",
            "Welcome back! As a treat, how about a 20% dicount? Use: FREESTUFF10 on your next order 😊",
            "Today is your lucky day! Use CODE50 on your next order for a 10% discount",
            "Thank you for your message, someone will be with your shortly"]




app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configuration for using a sqlite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# Creates an SQLAlchemy instance
db = SQLAlchemy(app)

# Data Class - Row data
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(5, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class ShoppingBasket(db.Model):
    __tablename__ = 'shopping_basket'
    id = db.Column(db.Integer, primary_key = True)
    session_id = db.Column(db.String(255), nullable=True)
    total = db.Column(db.Numeric(5, 2), default = 0)
    items = db.relationship('BasketItem', backref='basket', lazy=True)
    
class BasketItem(db.Model):
    __tablename__ = 'basket_item'
    id = db.Column(db.Integer, primary_key = True)
    basket_id = db.Column(db.Integer, db.ForeignKey('shopping_basket.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Numeric(5, 2), nullable=False)
    product = db.relationship('Product', backref='basket_items')

tables_created = False

@app.before_request
def create_tables():
    global tables_created
    if not tables_created:
        db.create_all()
        tables_created = True



@app.route("/")
def main():

    products = [
        {'name': 'MillaMia Naturally Soft Super Chunky', 'price': 10.50, 'stock': 10},
        {'name': 'Baa Ram Ewe DK', 'price': 14.99, 'stock': 5},
        {'name': 'Stylecraft Special DK Yarn', 'price': 2.35, 'stock': 20},
        {'name': 'James C Brett Craft Cotton DK', 'price': 1.69, 'stock': 2},
        {'name': 'Scheepjes Sugar Rush', 'price': 2.89, 'stock': 5},
        {'name': 'Anchor Baby Pure Cotton', 'price': 3.69, 'stock': 20},
        {'name': 'Bernat Blanket Big', 'price': 11.99, 'stock': 12},
        {'name': 'Caron Simply Soft Freckle Stripes', 'price': 5.49, 'stock': 9},
        {'name': 'Tulip Etimo Steel Softgrip Crochet Hook (1mm)', 'price': 8.79, 'stock': 9},
        {'name': 'Tulip Tunisian Crochet Hook Shanks - Bamboo (4.50mm)', 'price': 8.29, 'stock': 19},
        {'name': 'Pony Single End Crochet Hook - Maple (10.00mm)', 'price': 4.59, 'stock': 10},
        {'name': 'Bobbin Box Single End Crochet Hooks Set of 12', 'price': 9.99, 'stock': 3},
        {'name': 'KnitPro Crochet Hooks and Case', 'price': 29.99, 'stock': 2},
        {'name': 'Pumpkin - by Luluslittleshop', 'price': 2.88, 'stock': 5},
        {'name': 'Colourful Mini Dino', 'price': 0, 'stock': 500},
        {'name': 'Margo Barbie Jumper', 'price': 0, 'stock': 20},
        {'name': 'Playful Posy Blanket and Cushion', 'price': 2.79, 'stock': 5},
        {'name': 'Mikki CHUNKY Simple Rib Hat', 'price': 4.00, 'stock': 10}
    ]

    # Loop through list and add each product to Product table
    for product in products:
        existing_product = Product.query.filter_by(name = product['name']).first()
        # If the product doesn't exist then add a product to the database
        if not existing_product:
            new_product = Product(
                name = product['name'],
                price = product['price'],
                stock = product['stock']
            )
            db.session.add(new_product)

    db.session.commit()
    return render_template("index.html")


@app.route("/yarn", methods=["GET", "POST"])
def yarn():
    
    products = Product.query.all()

    if request.method =="POST":
        # Recieve product ID and quantity from form
        product_id = request.form.get("product_id")
        quantity = request.form.get("quantity", type = int)

        # Check if user has as session ID
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())

        session_id = session['session_id']

        # Add item to shopping basket
        basket = ShoppingBasket.query.filter_by(session_id=session_id).first()
        if not basket:
            # Create a new basket if it doesn't exist
            basket = ShoppingBasket(session_id=session_id)
            db.session.add(basket)
            db.session.commit()

        # Create new basket item
        basket_item = BasketItem(
            basket_id=basket.id,
            product_id=product_id,
            quantity=quantity,
            price=Product.query.get(product_id).price
    )
        db.session.add(basket_item)
        db.session.commit()

        # Redirect to basket after adding item
        return redirect(url_for('basket'))

    return render_template("yarn.html", products=products)

@app.route("/chatbox", methods=["GET", "POST"])
def chat_box():

    waiting = "Our offices are open Mon-Fri 8am-6pm, please leave a message and someone will be with you as soon as possible."

    if "userMsgs" not in session:
        # Empty session list to store user messages
        session["userMsgs"] = []

    # Default value of the variable when the page loads and there is no message generated
    randomMessage = ""

    if request.method == "POST":
        # Recieve value from user input
        userInput = request.form.get("message", "")

        if userInput:
            # Push the user's messages into the session list
            session["userMsgs"].append(userInput)
            # Generate random message in the variable
            randomMessage = random.choice(messagesList)

    return render_template("chatbox.html", userMsgs=session["userMsgs"], randomMessage=randomMessage, waiting=waiting)

@app.route("/basket", methods=["GET", "POST"])
def basket():

    # Check if session_id exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    # Grab current session ID
    session_id = session['session_id']

    # Use session ID to grab basket
    basket = ShoppingBasket.query.filter_by(session_id = session_id).first()


    if request.method == "POST":
        product_id = request.form.get("product_id")   
        if "update-basket" in request.form:
            # Update quantity
            new_quantity = int(request.form.get("quantity"))
            basket_item = BasketItem.query.filter_by(basket_id=basket.id, product_id=product_id).first()
            if basket_item:
                # Update quantity and price in database
                basket_item.quantity = new_quantity
                basket_item.price = basket_item.product.price * new_quantity
                db.session.commit()

        elif "delete-from-basket" in request.form:
            # Remove item from basket
            basket_item = BasketItem.query.filter_by(basket_id=basket.id, product_id=product_id).first()
            if basket_item:
                db.session.delete(basket_item)
                db.session.commit()
    # Grab items in basket if it exists
    items = []
    total = 0

    if basket:
        items = BasketItem.query.filter_by(basket_id = basket.id).all()
        total = sum(item.quantity * item.price for item in items)
        # Adds up each item added to basket
        
    return render_template("basket.html", items = items, total = total)



if __name__ in "__main__":
    app.run()