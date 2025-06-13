# shop_app/web_pages.py

import os
from flask import Flask, request, redirect, url_for, session, flash, get_flashed_messages
import dominate
from dominate.tags import *
from shared import database as db

# --- Flask App Initialization ---
static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
app = Flask(__name__, static_folder=static_folder_path, static_url_path='/static')
app.secret_key = 'a-super-secret-key-for-development-change-me' # REQUIRED for sessions and flash messages

# --- Base Page Structure ---
def create_base_page(page_title, content_func, show_back_button=True):
    doc = dominate.document(title=page_title)
    with doc.head:
        meta(charset="UTF-8")
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        link(rel="stylesheet", href="/static/css/style.css")
    
    with doc.body:
        with div(cls="container"):
            # --- Top Navigation with Back button and User Info ---
            with div(cls="top-nav"):
                if show_back_button:
                    a("← Back to Home", href=url_for('home'), cls="back-button")
                else:
                    span() # Empty span to keep alignment
                
                if 'user_name' in session:
                    with p(cls="user-info"):
                        span(f"Hi, {session['user_name']}!")
                        a("Logout", href=url_for('logout'))
            
            # --- Flash Messages ---
            for category, message in get_flashed_messages(with_categories=True):
                div(message, cls=f"flash-message flash-{category}")

            # Page content is rendered here
            content_func(app)
            
    return doc.render()

# --- Page Content Generators ---

# NEW: Login Page Content
def login_content(_):
    img(src="/static/images/pup_logo.png", cls="logo")
    h1("Mula sayo para sa bayan", style="color: #8c1515;")
    
    with div(cls="form-container"):
        with form(action=url_for('login'), method="post"):
            h2("Login")
            label("Email Address:", _for="email")
            input_(type="email", id="email", name="email", required=True)
            label("Password:", _for="password")
            input_(type="password", id="password", name="password", required=True)
            button("LOGIN", type="submit", cls="btn btn-primary btn-login-page")
        
        hr() # Separator
        p("Don't have an account?")
        a("REGISTER now", href=url_for('register_page'), cls="btn btn-secondary btn-login-page")

# NEW: Registration Page Content (Matches Image 1)
def registration_content(_):
    img(src="/static/images/pup_logo.png", cls="logo")
    h1("Mula sayo para sa bayan", style="color: #8c1515;")
    
    with div(cls="form-container"):
        with form(action=url_for('handle_register'), method="post"):
            h2("Register") # Matches your image layout implicitly
            label("Name:", _for="name")
            input_(type="text", id="name", name="name", required=True)
            label("Email Address:", _for="email")
            input_(type="email", id="email", name="email", required=True)
            label("Password:", _for="password")
            input_(type="password", id="password", name="password", required=True)
            label("Confirm Password:", _for="confirm_password")
            input_(type="password", id="confirm_password", name="confirm_password", required=True)
            
            # Buttons as per Image 1
            button("REGISTER", type="submit", cls="btn btn-register-page")
            a("Back to LOGIN", href=url_for('login_page'), cls="btn btn-login-page") # Link, not button
    
    # Add the '?' icon (placeholder for now)
    div("?", cls="question-mark-icon", style="position: absolute; bottom: 20px; right: 20px; font-size: 30px; font-weight: bold; color: #4a4a4a;")


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

def product_detail_content(product):
    if not product:
        h1("Product not found")
        return

    img(src=product['image_url'], style="max-width: 80%; border-radius: 8px;")
    h1(product['name'])
    h2(f"₱{product['price']:.2f}", style="color: #ff5722;")
    p(f"{product['sold_count']} sold")
    p(product['description'])

    p("Guaranteed to get by: 2-3 Days")
    p("✓ Free & Easy Return")

    with form(action=url_for('add_to_cart'), method="post"):
        input_(type="hidden", name="product_id", value=product['id'])
        if product.get('variations'):
            label("Select Variation:")
            select_tag = select(name="variation")
            with select_tag:
                for var in product['variations'].split(','):
                    option(var, value=var)
        
        button("ADD TO CART", type="submit", cls="btn-primary")
        button("BUY NOW", type="submit", cls="btn-secondary")

# Fully Functional Cart Page
def cart_content(_):
    h1("Shopping Cart")
    
    cart_items = session.get('cart', {})
    if not cart_items:
        p("Your cart is empty.")
        a("Go Shopping", href=url_for('home'), cls="btn btn-primary")
        return

    total_price = 0
    with div(cls="cart-container"):
        # Display each item in the cart
        for product_id_str, quantity in cart_items.items():
            try:
                product_id = int(product_id_str) # Convert key back to int
            except ValueError:
                continue # Skip invalid product_id in session
            
            product = db.get_product_by_id(product_id)
            if product:
                item_total = product['price'] * quantity
                total_price += item_total
                with div(cls="cart-item"):
                    img(src=product['image_url'])
                    with div(cls="cart-item-details"):
                        h3(product['name'])
                        p(f"Price: ₱{product['price']:.2f}")
                        with div(cls="quantity-control"):
                            a("-", href=url_for('update_cart_quantity', product_id=product_id, action='decrement'))
                            span(str(quantity))
                            a("+", href=url_for('update_cart_quantity', product_id=product_id, action='increment'))
                        p(f"Item Total: ₱{item_total:.2f}")
                        a("Remove", href=url_for('remove_from_cart', product_id=product_id))

    hr()
    h2(f"Total: ₱{total_price:.2f}")
    a("CHECK OUT (WIP)", href="#", cls="btn btn-checkout")

def profile_content(_):
    h1("User Profile")
    with div(cls="profile-section", style="text-align: left;"):
        img(src="/static/images/user_icon.png", style="width: 80px; height: 80px; display: block; margin: 0 auto 20px; border-radius: 50%; border: 2px solid #8c1515;")
        if 'user_name' in session:
            h3(session['user_name'])
        
        h4("Address: 1")
        p("Name: John Doe")
        p("Contact No.: +639123456789")
        
        h4("Address: 2")
        p("Name: Jane Smith")
        p("Contact No.: +639987654321")
    
    a("Order History", href=url_for('order_history'))
    br()
    a("Contact Us", href=url_for('contact_us'))
    br()
    a("Logout", href=url_for('logout'))


def order_history_content(_):
    h1("Order History")
    # Placeholder data for order history
    with table(cls="admin-table"):
        with thead():
            with tr():
                th("Ref No.")
                th("Order Status")
                th("Quantity")
                th("Payment")
        with tbody():
            with tr():
                td("ORD-20250613-001")
                td("Delivered")
                td("2 items")
                td("₱320.00 (COD)")
            with tr():
                td("ORD-20250610-002")
                td("Processing")
                td("1 item")
                td("₱450.00 (COD)")
            with tr():
                td("ORD-20250605-003")
                td("Cancelled")
                td("3 items")
                td("₱600.00 (COD)")


def contact_us_content(_):
    h1("Contact Us")
    with form(action=url_for('handle_feedback'), method="post"):
        label("Name:")
        input_(type="text", name="name")
        label("Email Address:")
        input_(type="email", name="email")
        label("Message:")
        textarea(name="message", rows="5")
        button("Submit", type="submit", cls="btn-primary")

# --- Flask Routes ---

# NEW: Login Page (Root)
@app.route('/')
def login_page():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return create_base_page("Welcome", login_content, show_back_button=False)

# NEW: Login POST Handler
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = db.get_user_by_email(email)
    
    if user and db.check_password(user['password_hash'], password):
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session.setdefault('cart', {}) # Initialize cart if not exists
        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Login failed. Please check your email and password.', 'error')
        return redirect(url_for('login_page'))

# NEW: Registration Page (GET)
@app.route('/register')
def register_page():
    if 'user_id' in session: # If already logged in, no need to register
        return redirect(url_for('home'))
    return create_base_page("Register", registration_content, show_back_button=False)

# NEW: Registration POST Handler
@app.route('/register', methods=['POST'])
def handle_register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        flash("Passwords do not match.", 'error')
        return redirect(url_for('register_page'))

    success, message = db.create_user(name, email, password)
    if success:
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login_page'))
    else:
        if "Duplicate entry" in message and "for key 'users.email'" in message:
            flash("Registration failed: Email already registered.", 'error')
        else:
            flash(f"Registration failed: {message}", 'error')
        return redirect(url_for('register_page'))

# Route protection decorator (DRY principle)
def login_required(f):
    @dominate.util.make_tag_function
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/home')
@login_required
def home():
    return create_base_page("Homepage", homepage_content)

@app.route('/product/<int:product_id>')
@login_required
def product_detail(product_id):
    product = db.get_product_by_id(product_id)
    return create_base_page(product['name'] if product else "Not Found", lambda _: product_detail_content(product))

@app.route('/cart')
@login_required
def cart():
    return create_base_page("Shopping Cart", cart_content)

@app.route('/profile')
@login_required
def profile():
    return create_base_page("Profile", profile_content)

@app.route('/order-history')
@login_required
def order_history():
    return create_base_page("Order History", order_history_content)
    
@app.route('/contact')
@login_required
def contact_us():
    return create_base_page("Contact Us", contact_us_content)

@app.route('/logout')
def logout():
    session.clear() # Clears all session data
    flash('You have been logged out.', 'success')
    return redirect(url_for('login_page'))

@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('product_id')
    # Convert product_id to string for consistent session keys
    product_id_str = str(product_id) 
    
    cart = session.get('cart', {})
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    session['cart'] = cart # Update the session dict
    session.modified = True # Important: Flask needs this for mutable session changes
    
    flash(f"Item added to cart!", 'success')
    return redirect(url_for('cart'))

@app.route('/remove-from-cart/<product_id>')
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if product_id in cart:
        cart.pop(product_id, None)
        session['cart'] = cart
        session.modified = True
        flash('Item removed from cart.', 'success')
    return redirect(url_for('cart'))

@app.route('/update-cart-quantity/<product_id>/<action>')
@login_required
def update_cart_quantity(product_id, action):
    cart = session.get('cart', {})
    if product_id in cart:
        if action == 'increment':
            cart[product_id] += 1
        elif action == 'decrement':
            if cart[product_id] > 1:
                cart[product_id] -= 1
            else: # If quantity is 1 and decremented, remove item
                cart.pop(product_id, None)
        
        session['cart'] = cart
        session.modified = True
        
    return redirect(url_for('cart'))

# (Other routes like contact_us and product_detail_content can remain as they are)
@app.route('/submit-feedback', methods=['POST'])
@login_required
def handle_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    print(f"Feedback Received:\nName: {name}\nEmail: {email}\nMessage: {message}")
    flash('Your feedback has been submitted!', 'success')
    return redirect(url_for('home'))