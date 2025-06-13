# shop_app/web_pages.py

import os
from flask import Flask, request, redirect, url_for, session, flash
import dominate
from dominate.tags import *
from shared import database as db

# --- Flask App Initialization ---
static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
app = Flask(__name__, static_folder=static_folder_path, static_url_path='/static')
# SECRET_KEY is required for session management
app.secret_key = 'a-super-secret-key-for-development-change-me'

# --- Base Page Structure ---
def create_base_page(page_title, content_func):
    doc = dominate.document(title=page_title)
    with doc.head:
        meta(charset="UTF-8")
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        link(rel="stylesheet", href="/static/css/style.css")
    
    with doc.body:
        with div(cls="container"):
            # --- NEW: Top Navigation with Back button and User Info ---
            with div(cls="top-nav"):
                if page_title not in ["Welcome", "Homepage"]:
                    a("← Back to Home", href=url_for('home'), cls="back-button")
                else:
                    span() # Empty span to keep alignment
                
                if 'user_name' in session:
                    with p(cls="user-info"):
                        span(f"Hi, {session['user_name']}!")
                        a("Logout", href=url_for('logout'))
            
            # Page content is rendered here
            content_func(app)
            
    return doc.render()

# --- Page Content Generators ---
def login_register_content(_):
    img(src="/static/images/pup_logo.png", cls="logo")
    h1("Mula sayo para sa bayan", style="color: #8c1515;")
    
    # --- NEW: Login Form ---
    with div(cls="form-container"):
        with form(action=url_for('login'), method="post"):
            h2("Login")
            label("Email Address:", _for="email")
            input_(type="email", id="email", name="email", required=True)
            label("Password:", _for="password")
            input_(type="password", id="password", name="password", required=True)
            button("LOGIN", type="submit", cls="btn-primary")
            
    # --- Updated: Register Form ---
    with div(cls="form-container"):
        with form(action=url_for('handle_register'), method="post"):
            h2("Register")
            label("Name:", _for="name")
            input_(type="text", id="name", name="name", required=True)
            label("Email Address:", _for="reg_email")
            input_(type="email", id="reg_email", name="email", required=True)
            label("Password:", _for="reg_password")
            input_(type="password", id="reg_password", name="password", required=True)
            button("REGISTER", type="submit", cls="btn-secondary")

def homepage_content(_):
    h1("Homepage")
    h2("Best Sellers")

    products = db.get_all_products()
    with div(cls="product-grid"):
        for product in products:
            with a(href=url_for('product_detail', product_id=product['id']), cls="product-item"):
                img(src=product['image_url'])
                h3(product['name'])
                p(f"₱{product['price']:.2f}")

# (product_detail_content remains the same, but will benefit from the new back button)

# --- NEW: Fully Functional Cart Page ---
def cart_content(_):
    h1("Shopping Cart")
    
    cart_items = session.get('cart', {})
    if not cart_items:
        p("Your cart is empty.")
        a("Go Shopping", href=url_for('home'), cls="btn btn-primary")
        return

    total_price = 0
    with div(cls="cart-container"):
        for product_id, quantity in cart_items.items():
            product = db.get_product_by_id(product_id)
            if product:
                item_total = product['price'] * quantity
                total_price += item_total
                with div(cls="cart-item"):
                    img(src=product['image_url'])
                    with div(cls="cart-item-details"):
                        h3(product['name'])
                        p(f"Quantity: {quantity} x ₱{product['price']:.2f} = ₱{item_total:.2f}")
                        a("Remove", href=url_for('remove_from_cart', product_id=product_id))

    hr()
    h2(f"Subtotal: ₱{total_price:.2f}")
    a("CHECK OUT (WIP)", href="#", cls="btn btn-checkout")

# --- Flask Routes ---
@app.route('/')
def login_register_page():
    # If user is already logged in, redirect to home
    if 'user_id' in session:
        return redirect(url_for('home'))
    return create_base_page("Welcome", login_register_content)

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login_register_page'))
    return create_base_page("Homepage", homepage_content)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login_register_page'))
    product = db.get_product_by_id(product_id)
    return create_base_page(product['name'] if product else "Not Found", lambda _: product_detail_content(product))

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login_register_page'))
    return create_base_page("Shopping Cart", cart_content)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login_register_page'))
    return create_base_page("Profile", lambda _: h1("Profile Page (WIP)"))

# --- NEW: Login/Logout and Cart Routes ---
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = db.get_user_by_email(email)
    
    if user and db.check_password(user['password_hash'], password):
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['cart'] = {} # Start with an empty cart on new login
        return redirect(url_for('home'))
    else:
        # Here you could flash a message
        print("Login failed for user:", email)
        return redirect(url_for('login_register_page'))

@app.route('/logout')
def logout():
    session.clear() # Clears all session data
    return redirect(url_for('login_register_page'))

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return redirect(url_for('login_register_page'))
        
    product_id = request.form.get('product_id')
    # Initialize cart if it doesn't exist
    if 'cart' not in session:
        session['cart'] = {}
        
    # Add item to cart or increment quantity
    session['cart'][product_id] = session['cart'].get(product_id, 0) + 1
    session.modified = True # Important to save session changes
    
    return redirect(url_for('cart'))

@app.route('/remove-from-cart/<product_id>')
def remove_from_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login_register_page'))
    
    if 'cart' in session and product_id in session['cart']:
        session['cart'].pop(product_id, None)
        session.modified = True
        
    return redirect(url_for('cart'))

# (Register route remains the same, but the form name is updated)
@app.route('/register', methods=['POST'])
def handle_register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    success, message = db.create_user(name, email, password)
    if not success:
        print(f"Registration failed: {message}")
    return redirect(url_for('login_register_page'))

# (Other routes like contact_us and product_detail_content can remain as they are)