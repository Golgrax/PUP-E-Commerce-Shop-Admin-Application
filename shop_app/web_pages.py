# shop_app/web_pages.py

import os
from flask import Flask, request, redirect, url_for, session, flash, get_flashed_messages
import dominate
from dominate.tags import *
from functools import wraps # For login_required decorator

from shared import database as db

# --- Flask App Initialization ---
static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
app = Flask(__name__, static_folder=static_folder_path, static_url_path='/static')
app.secret_key = 'a-super-secret-key-for-development-change-me' # REQUIRED for sessions and flash messages

# --- Constants for PUP Colors ---
PUP_BURGUNDY = '#722F37'
PUP_GOLD = '#FFD700'
PUP_DARK_BURGUNDY = '#5A252A'
PUP_TEAL = '#00BCD4' # From previous design, for register button

# --- Login Required Decorator (FIXED) ---
def login_required(f):
    @wraps(f) # Important for preserving original function metadata
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# --- Base Page Structure (with Tailwind/Font Awesome Header and Nav) ---
def create_base_page(page_title, content_func, current_nav_item=None, show_header_nav=True):
    doc = dominate.document(title=f"PUP Mobile Store - {page_title}")
    with doc.head:
        meta(charset="UTF-8")
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css")
        link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css")
        link(rel="stylesheet", href="/static/css/style.css") # For custom font and variables

    with doc.body(cls="bg-gray-50 font-sans"):
        # Header
        if show_header_nav:
            with header(cls=f"bg-[{PUP_BURGUNDY}] text-white p-4 shadow-lg"):
                with div(cls="flex items-center justify-between"):
                    with div(cls="flex items-center space-x-3"):
                        with div(cls=f"w-10 h-10 bg-[{PUP_GOLD}] rounded-full flex items-center justify-center"):
                            i(cls="fas fa-star text-red-800")
                        with div():
                            h1("StudywithStyle", cls="text-lg font-bold")
                            p("PUP Official Store", cls="text-xs opacity-90")
                    with div(cls="flex space-x-3"):
                        with div(cls="relative"):
                            a(href=url_for('cart'), cls="p-2 bg-black bg-opacity-20 rounded-full"):
                                i(cls="fas fa-shopping-cart")
                            # Cart badge
                            total_cart_items = sum(session.get('cart', {}).values())
                            if total_cart_items > 0:
                                span(str(total_cart_items), id="cart-badge", cls="cart-badge")
                            else:
                                span(str(total_cart_items), id="cart-badge", cls="cart-badge", style="display: none;")
                        a(href=url_for('profile'), cls="p-2 bg-black bg-opacity-20 rounded-full"):
                            i(cls="fas fa-user")
        
        # Main Content Container
        with main(cls="content-container p-4"):
            # Flash messages (style them with Tailwind using .flash-success, .flash-error)
            for category, message in get_flashed_messages(with_categories=True):
                div(message, cls=f"p-3 mb-4 rounded-lg font-semibold text-sm flash-{category}")

            # Page-specific content
            content_func(app)

        # Bottom Navigation
        if show_header_nav:
            with nav(cls=f"bottom-nav bg-[{PUP_BURGUNDY}] text-white"):
                with div(cls="flex justify-around items-center py-3"):
                    with a(href=url_for('home'), cls=f"nav-btn flex flex-col items-center space-y-1 {'opacity-75' if current_nav_item != 'home' else ''}"):
                        i(cls="fas fa-home text-xl")
                        span("Home", cls="text-xs")
                    with a(href=url_for('cart'), cls=f"nav-btn flex flex-col items-center space-y-1 relative {'opacity-75' if current_nav_item != 'cart' else ''}"):
                        i(cls="fas fa-shopping-cart text-xl")
                        span("Cart", cls="text-xs")
                        total_cart_items = sum(session.get('cart', {}).values())
                        if total_cart_items > 0:
                            span(str(total_cart_items), id="nav-cart-badge", cls="cart-badge")
                        else:
                            span(str(total_cart_items), id="nav-cart-badge", cls="cart-badge", style="display: none;")
                    with a(href=url_for('profile'), cls=f"nav-btn flex flex-col items-center space-y-1 {'opacity-75' if current_nav_item != 'profile' else ''}"):
                        i(cls="fas fa-user text-xl")
                        span("Profile", cls="text-xs")
        
        # Help Button (fixed position, from example)
        if show_header_nav:
            a(href=url_for('contact_us'), cls="fixed bottom-24 right-4 w-12 h-12 bg-black text-white rounded-full shadow-lg z-40 flex items-center justify-center"):
                i(cls="fas fa-question")

    return doc.render()

# --- Page Content Generators (Adapted to Tailwind CSS) ---

# Login Section (matches example's login section)
def login_content(_):
    with div(cls="text-center mb-6"):
        with div(cls=f"w-16 h-16 bg-[{PUP_GOLD}] rounded-full flex items-center justify-center mx-auto mb-4"):
            i(cls="fas fa-star text-red-800 text-2xl")
        h2("Welcome Back", cls=f"text-2xl font-bold text-[{PUP_BURGUNDY}]")

    with form(action=url_for('login'), method="post", cls="bg-white rounded-lg shadow-lg p-6"):
        with div(cls="mb-4"):
            label("Email Address:", cls="block text-gray-700 font-semibold mb-2", _for="email")
            input_(type="email", name="email", cls="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")
        with div(cls="mb-6"):
            label("Password:", cls="block text-gray-700 font-semibold mb-2", _for="password")
            input_(type="password", name="password", cls="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")

        with div(cls="space-y-3"):
            button("LOGIN", type="submit", cls=f"w-full bg-[{PUP_BURGUNDY}] text-white py-3 rounded-lg font-semibold hover:bg-[{PUP_DARK_BURGUNDY}] transition-colors")
            a("Create Account", href=url_for('register_page'), cls=f"w-full bg-[{PUP_TEAL}] text-white py-3 rounded-lg font-semibold hover:bg-cyan-500 transition-colors flex items-center justify-center")

# Registration Section (matches Image 1 exactly, with Tailwind)
def registration_content(_):
    with div(cls="text-center mb-6"):
        with div(cls=f"w-16 h-16 bg-[{PUP_GOLD}] rounded-full flex items-center justify-center mx-auto mb-4"):
            i(cls="fas fa-star text-red-800 text-2xl")
        h2("Mula sayo para sa bayan", cls=f"text-2xl font-bold text-[{PUP_BURGUNDY}]")

    with form(action=url_for('handle_register'), method="post", cls="bg-white rounded-lg shadow-lg p-6"):
        with div(cls="mb-4"):
            label("Name:", cls="block text-gray-700 font-semibold mb-2", _for="name")
            input_(type="text", name="name", cls="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")
        with div(cls="mb-4"):
            label("Email Address:", cls="block text-gray-700 font-semibold mb-2", _for="email")
            input_(type="email", name="email", cls="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")
        with div(cls="mb-4"):
            label("Password:", cls="block text-gray-700 font-semibold mb-2", _for="password")
            input_(type="password", name="password", cls="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")
        with div(cls="mb-6"):
            label("Confirm Password:", cls="block text-gray-700 font-semibold mb-2", _for="confirm_password")
            input_(type="password", name="confirm_password", cls="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")

        with div(cls="space-y-3"):
            # The "Back to LOGIN" button from image 1 is actually a link styled as a button
            a("Back to LOGIN", href=url_for('login_page'), cls=f"w-full bg-[{PUP_TEAL}] text-white py-3 rounded-lg font-semibold hover:bg-cyan-500 transition-colors flex items-center justify-center")
            button("REGISTER", type="submit", cls=f"w-full bg-[{PUP_TEAL}] text-white py-3 rounded-lg font-semibold hover:bg-cyan-600 transition-colors")
    
    # Question Mark button (as per image 1)
    a(href=url_for('contact_us'), cls="fixed bottom-4 right-4 w-12 h-12 bg-black text-white rounded-full shadow-lg z-40 flex items-center justify-center"):
        i(cls="fas fa-question text-xl")


# Homepage/Product Listing Section (matches example's homepage)
def homepage_content(_):
    with div(cls="mb-6"):
        h2("Featured Products", cls=f"text-2xl font-bold text-[{PUP_BURGUNDY}] mb-2")
        p("Official PUP merchandise and study essentials", cls="text-gray-600")

    # Featured Product (from example)
    with div(cls="bg-white rounded-lg shadow-lg p-4 mb-6"):
        with div(cls="flex items-start space-x-4"):
            # Placeholder for product image. Replace with actual image.
            img(src="/static/images/product_lanyard_1.png", cls=f"w-24 h-24 bg-[{PUP_BURGUNDY}] rounded-lg object-cover")
            with div(cls="flex-1"):
                h3("PUP STUDY WITH STYLE Baybayin - Classic Edition", cls=f"font-bold text-[{PUP_BURGUNDY}] text-lg")
                p("Polytechnic University (PUP) Lanyard", cls="text-sm text-gray-600 mb-2")
                with div(cls="flex items-center justify-between"):
                    span("₱140", cls=f"text-2xl font-bold text-[{PUP_BURGUNDY}]")
                    with form(action=url_for('add_to_cart'), method="post", style="display:inline;"):
                        input_(type="hidden", name="product_id", value="1") # Assuming ID 1 for this lanyard
                        button("ADD TO CART", type="submit", cls="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-full font-bold transition-colors")

    # You Might Like Section (from example, using actual products from DB)
    with div(cls="mb-6"):
        h3("You Might Like", cls=f"text-xl font-bold text-[{PUP_BURGUNDY}] mb-4")
        with div(cls="grid grid-cols-1 gap-4"):
            products = db.get_all_products() # Get all products for "You Might Like"
            for product in products:
                if product['id'] == 1: continue # Skip the featured product if it's there
                with div(cls="bg-white rounded-lg shadow-md p-4 product-card"):
                    with div(cls="flex items-center space-x-4"):
                        img(src=product['image_url'], cls=f"w-16 h-16 bg-[{PUP_BURGUNDY}] rounded-lg flex items-center justify-center text-white object-cover") # Use actual image
                        with div(cls="flex-1"):
                            h4(product['name'], cls=f"font-semibold text-[{PUP_BURGUNDY}]")
                            p(product['description'], cls="text-sm text-gray-600")
                            with div(cls="flex justify-between items-center mt-2"):
                                span(f"₱{product['price']:.2f}", cls=f"font-bold text-[{PUP_BURGUNDY}]")
                                with form(action=url_for('add_to_cart'), method="post", style="display:inline;"):
                                    input_(type="hidden", name="product_id", value=str(product['id']))
                                    button("ADD TO CART", type="submit", cls="bg-red-500 text-white px-4 py-1 rounded-full text-sm")

# Product Detail Page (adapted to Tailwind)
def product_detail_content(product):
    if not product:
        h1("Product not found", cls=f"text-2xl font-bold text-[{PUP_BURGUNDY}]")
        return

    with div(cls="bg-white rounded-lg shadow-lg p-4 mb-6"):
        img(src=product['image_url'], cls="w-full max-h-64 object-cover rounded-lg mb-4")
        h1(product['name'], cls=f"text-2xl font-bold text-[{PUP_BURGUNDY}] mb-2")
        h2(f"₱{product['price']:.2f}", cls="text-3xl font-bold text-red-500 mb-2")
        p(f"{product['sold_count']} sold", cls="text-gray-600 text-sm mb-4")
        p(product['description'], cls="text-gray-700 mb-4")

        with div(cls="text-sm text-gray-600 mb-4"):
            p("Guaranteed to get by: 2-3 Days")
            p("✓ Free & Easy Return")
            p("✓ Merchandise Protection")

        if product.get('variations'):
            with div(cls="mb-6"):
                label("Select Variation:", cls="block text-gray-700 font-semibold mb-2")
                select_tag = select(name="variation", cls="w-full p-2 border border-gray-300 rounded-lg")
                with select_tag:
                    for var in product['variations'].split(','):
                        option(var, value=var)
        
        with div(cls="flex space-x-4"):
            with form(action=url_for('add_to_cart'), method="post", cls="flex-1"):
                input_(type="hidden", name="product_id", value=str(product['id']))
                button("ADD TO CART", type="submit", cls="w-full bg-red-500 hover:bg-red-600 text-white py-3 rounded-lg font-bold transition-colors")
            with form(action=url_for('add_to_cart'), method="post", cls="flex-1"): # For demo, BUY NOW also adds to cart
                input_(type="hidden", name="product_id", value=str(product['id']))
                button("BUY NOW", type="submit", cls=f"w-full bg-[{PUP_BURGUNDY}] hover:bg-[{PUP_DARK_BURGUNDY}] text-white py-3 rounded-lg font-bold transition-colors")

# Shopping Cart Section (fully functional with Tailwind)
def cart_content(_):
    h2("Shopping Cart", cls=f"text-2xl font-bold text-[{PUP_BURGUNDY}] mb-4")
    
    with div(cls=f"bg-gradient-to-r from-[{PUP_GOLD}] to-orange-400 rounded-lg p-4 mb-6"):
        with div(cls="text-center"):
            h3("POLYTECHNIC UNIVERSITY OF THE PHILIPPINES", cls="font-bold text-white text-lg mb-2")
            with div(cls="bg-white bg-opacity-20 rounded p-2 inline-block"):
                i(cls="fas fa-university text-white text-2xl")

    cart_items = session.get('cart', {})
    total_price = 0

    with div(id="cart-items", cls="space-y-4 mb-6"):
        if not cart_items:
            with div(cls="text-center text-gray-500 py-8"):
                i(cls="fas fa-shopping-cart text-4xl mb-4")
                p("Your cart is empty")
        else:
            for product_id_str, quantity in cart_items.items():
                try:
                    product_id = int(product_id_str)
                except ValueError:
                    continue # Skip invalid product_id
                
                product = db.get_product_by_id(product_id)
                if product:
                    item_total = product['price'] * quantity
                    total_price += item_total
                    with div(cls="bg-white rounded-lg shadow-md p-4"):
                        with div(cls="flex items-center justify-between"):
                            with div(cls="flex items-center space-x-3"):
                                input_(type="checkbox", checked=True, cls="w-4 h-4 text-red-500")
                                img(src=product['image_url'], cls=f"w-12 h-12 bg-[{PUP_BURGUNDY}] rounded object-cover flex items-center justify-center text-white")
                                with div():
                                    h4(product['name'], cls=f"font-semibold text-[{PUP_BURGUNDY}] text-sm")
                                    p(f"₱{product['price']:.2f}", cls="text-gray-600 text-xs")
                            with div(cls="flex items-center space-x-2"):
                                a(href=url_for('update_cart_quantity', product_id=product_id, action='decrement'),
                                  cls="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center"):
                                    i(cls="fas fa-minus text-xs")
                                span(str(quantity), cls="w-8 text-center font-semibold")
                                a(href=url_for('update_cart_quantity', product_id=product_id, action='increment'),
                                  cls="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center"):
                                    i(cls="fas fa-plus text-xs")
                                a(href=url_for('remove_from_cart', product_id=product_id),
                                  cls="text-red-500 hover:text-red-700 ml-2"):
                                    i(cls="fas fa-trash-alt text-base")

    # Cart Summary
    with div(id="cart-summary", cls="bg-white rounded-lg shadow-lg p-4 mb-6" if cart_items else "hidden"):
        with div(cls=f"flex justify-between items-center text-lg font-bold text-[{PUP_BURGUNDY}]"):
            span("Total:")
            span(f"₱{total_price:.2f}", id="cart-total")

    button("CHECK OUT", onclick="alert('Checkout functionality is a work in progress!');",
           cls=f"w-full bg-[{PUP_BURGUNDY}] text-white py-4 rounded-lg font-bold text-lg {'hidden' if not cart_items else ''}")


# Contact Section (matches example's contact section)
def contact_us_content(_):
    with div(cls="text-center mb-6"):
        with div(cls=f"w-16 h-16 bg-[{PUP_GOLD}] rounded-full flex items-center justify-center mx-auto mb-4"):
            i(cls="fas fa-star text-red-800 text-2xl")
        h2("Contact Us", cls=f"text-2xl font-bold text-[{PUP_BURGUNDY}]")

    with form(action=url_for('handle_feedback'), method="post", cls="bg-white rounded-lg shadow-lg p-6"):
        with div(cls="mb-4"):
            label("Name:", cls="block text-gray-700 font-semibold mb-2", _for="name")
            input_(type="text", name="name", cls="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")
        with div(cls="mb-4"):
            label("Email Address:", cls="block text-gray-700 font-semibold mb-2", _for="email")
            input_(type="email", name="email", cls="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")
        with div(cls="mb-6"):
            with div(cls="flex items-center mb-2"):
                label("Message", cls="text-gray-700 font-semibold", _for="message")
                i(cls="fas fa-question-circle text-gray-400 ml-2")
            textarea(name="message", rows="4", cls="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500 resize-none")
        button("Submit", type="submit", cls=f"w-full bg-[{PUP_BURGUNDY}] text-white py-3 rounded-lg font-semibold border-2 border-[{PUP_BURGUNDY}] hover:bg-white hover:text-red-800 transition-colors")


# Profile Section (matches example's profile section)
def profile_content(_):
    with div(cls="text-center mb-6"):
        with div(cls="w-20 h-20 bg-gray-300 rounded-full flex items-center justify-center mx-auto mb-4"):
            # Ensure you have assets/images/user_icon.png or change this icon
            i(cls="fas fa-user text-3xl text-gray-600") # Replace with img if you have user_icon.png
        h2(session.get('user_name', 'Guest'), cls=f"text-2xl font-bold text-[{PUP_BURGUNDY}]")

    with div(cls="bg-white rounded-lg shadow-lg p-6 mb-6"):
        with div(cls="space-y-4"):
            with a(href="#", cls="flex items-center justify-between p-3 border-b hover:bg-gray-50"): # Account Settings
                span("Account Settings", cls="font-semibold")
                i(cls="fas fa-chevron-right text-gray-400")
            with a(href=url_for('order_history'), cls="flex items-center justify-between p-3 border-b hover:bg-gray-50"): # Order History
                span("Order History", cls="font-semibold")
                i(cls="fas fa-chevron-right text-gray-400")
            with a(href="#", cls="flex items-center justify-between p-3 border-b hover:bg-gray-50"): # Favorites
                span("Favorites", cls="font-semibold")
                i(cls="fas fa-chevron-right text-gray-400")
            with a(href=url_for('contact_us'), cls="flex items-center justify-between p-3 hover:bg-gray-50"): # Help & Support
                span("Help & Support", cls="font-semibold")
                i(cls="fas fa-chevron-right text-gray-400")

    with div(cls="space-y-3"):
        # Display Sign Out button if logged in
        if 'user_id' in session:
            a("Sign Out", href=url_for('logout'), cls=f"w-full bg-[{PUP_BURGUNDY}] text-white py-3 rounded-lg font-semibold flex items-center justify-center")
        else:
            # Otherwise, display Sign In and Create Account buttons
            a("Sign In", href=url_for('login_page'), cls=f"w-full bg-[{PUP_BURGUNDY}] text-white py-3 rounded-lg font-semibold flex items-center justify-center")
            a("Create Account", href=url_for('register_page'), cls="w-full bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold flex items-center justify-center")

# Order History Section (adapted to Tailwind)
def order_history_content(_):
    h1("Order History", cls=f"text-2xl font-bold text-[{PUP_BURGUNDY}] mb-4")
    
    with div(cls="bg-white rounded-lg shadow-lg p-6"):
        with table(cls="min-w-full divide-y divide-gray-200"):
            with thead(cls=f"bg-[{PUP_BURGUNDY}]"):
                with tr():
                    th("Ref No.", cls="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
                    th("Order Status", cls="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
                    th("Quantity", cls="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
                    th("Payment", cls="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
            with tbody(cls="bg-white divide-y divide-gray-200"):
                with tr():
                    td("ORD-20250613-001", cls="px-4 py-2 whitespace-nowrap text-sm text-gray-900")
                    td("Delivered", cls="px-4 py-2 whitespace-nowrap text-sm text-green-600 font-semibold")
                    td("2 items", cls="px-4 py-2 whitespace-nowrap text-sm text-gray-500")
                    td("₱320.00 (COD)", cls="px-4 py-2 whitespace-nowrap text-sm text-gray-500")
                with tr():
                    td("ORD-20250610-002", cls="px-4 py-2 whitespace-nowrap text-sm text-gray-900")
                    td("Processing", cls="px-4 py-2 whitespace-nowrap text-sm text-blue-600 font-semibold")
                    td("1 item", cls="px-4 py-2 whitespace-nowrap text-sm text-gray-500")
                    td("₱450.00 (COD)", cls="px-4 py-2 whitespace-nowrap text-sm text-gray-500")
                with tr():
                    td("ORD-20250605-003", cls="px-4 py-2 whitespace-nowrap text-sm text-gray-900")
                    td("Cancelled", cls="px-4 py-2 whitespace-nowrap text-sm text-red-600 font-semibold")
                    td("3 items", cls="px-4 py-2 whitespace-nowrap text-sm text-gray-500")
                    td("₱600.00 (COD)", cls="px-4 py-2 whitespace-nowrap text-sm text-gray-500")

# --- Flask Routes ---

@app.route('/')
def login_page():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return create_base_page("Login", login_content, show_header_nav=False)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = db.get_user_by_email(email)
    
    if user and db.check_password(user['password_hash'], password):
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session.setdefault('cart', {})
        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Login failed. Please check your email and password.', 'error')
        return redirect(url_for('login_page'))

@app.route('/register')
def register_page():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return create_base_page("Register", registration_content, show_header_nav=False)

@app.route('/register', methods=['POST'])
def handle_register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not (name and email and password and confirm_password):
        flash("All fields are required.", 'error')
        return redirect(url_for('register_page'))

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

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login_page'))

@app.route('/home')
@login_required
def home():
    return create_base_page("Home", homepage_content, current_nav_item='home')

@app.route('/product/<int:product_id>')
@login_required
def product_detail(product_id):
    product = db.get_product_by_id(product_id)
    # Note: No 'Back to Home' explicit button here, relies on bottom nav or browser back.
    return create_base_page("Product Detail", lambda _: product_detail_content(product))

@app.route('/cart')
@login_required
def cart():
    return create_base_page("Cart", cart_content, current_nav_item='cart')

@app.route('/profile')
@login_required
def profile():
    return create_base_page("Profile", profile_content, current_nav_item='profile')

@app.route('/order-history')
@login_required
def order_history():
    return create_base_page("Order History", order_history_content)
    
@app.route('/contact')
@login_required
def contact_us():
    return create_base_page("Contact Us", contact_us_content)

@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1)) # Allow adding more than 1 if needed
    
    product_id_str = str(product_id) 
    cart = session.get('cart', {})
    cart[product_id_str] = cart.get(product_id_str, 0) + quantity
    session['cart'] = cart
    session.modified = True
    
    flash(f"'{db.get_product_by_id(product_id)['name']}' added to cart!", 'success')
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

@app.route('/submit-feedback', methods=['POST'])
@login_required
def handle_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    print(f"Feedback Received:\nName: {name}\nEmail: {email}\nMessage: {message}")
    flash('Your feedback has been submitted!', 'success')
    return redirect(url_for('home'))