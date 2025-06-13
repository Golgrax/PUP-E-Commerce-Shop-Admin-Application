# shop_app/web_pages.py

import os
from flask import Flask, request, redirect, url_for, session, flash, get_flashed_messages
import dominate
from dominate.tags import *
from functools import wraps # Correct import for decorators

from shared import database as db

# --- Flask App Initialization ---
static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
app = Flask(__name__, static_folder=static_folder_path, static_url_path='/static')
app.secret_key = 'a-super-secret-key-for-development-change-me' # REQUIRED for sessions and flash messages

# --- Constants for PUP Colors ---
PUP_BURGUNDY = '#722F37'
PUP_GOLD = '#FFD700'
PUP_DARK_BURGUNDY = '#5A252A'
PUP_TEAL = '#00BCD4' # From previous design, kept for "REGISTER" button

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

    with doc.body(_class="bg-gray-50 font-sans"): # Changed cls to _class
        # Header
        if show_header_nav:
            with header(_class=f"bg-[{PUP_BURGUNDY}] text-white p-4 shadow-lg"): # Changed cls to _class
                with div(_class="flex items-center justify-between"): # Changed cls to _class
                    with div(_class="flex items-center space-x-3"): # Changed cls to _class
                        with div(_class=f"w-10 h-10 bg-[{PUP_GOLD}] rounded-full flex items-center justify-center"): # Changed cls to _class
                            i(_class="fas fa-star text-red-800") # Changed cls to _class
                        with div():
                            h1("StudywithStyle", _class="text-lg font-bold") # Changed cls to _class
                            p("PUP Official Store", _class="text-xs opacity-90") # Changed cls to _class
                    with div(_class="flex space-x-3"): # Changed cls to _class
                        with div(_class="relative"): # Changed cls to _class
                            # FIX: Removed the colon here
                            a(href=url_for('cart'), _class="p-2 bg-black bg-opacity-20 rounded-full")( # Changed cls to _class
                                i(_class="fas fa-shopping-cart") # Changed cls to _class
                            )
                            # Cart badge
                            total_cart_items = sum(session.get('cart', {}).values())
                            if total_cart_items > 0:
                                span(str(total_cart_items), id="cart-badge", _class="cart-badge") # Changed cls to _class
                            else:
                                span(str(total_cart_items), id="cart-badge", _class="cart-badge", style="display: none;") # Changed cls to _class
                        a(href=url_for('profile'), _class="p-2 bg-black bg-opacity-20 rounded-full"): # Changed cls to _class
                            i(_class="fas fa-user") # Changed cls to _class
        
        # Main Content Container
        with main(_class="content-container p-4"): # Changed cls to _class
            # Flash messages (style them with Tailwind using .flash-success, .flash-error)
            for category, message in get_flashed_messages(with_categories=True):
                div(message, _class=f"p-3 mb-4 rounded-lg font-semibold text-sm flash-{category}") # Changed cls to _class

            # Page-specific content
            content_func(app)

        # Bottom Navigation
        if show_header_nav:
            with nav(_class=f"bottom-nav bg-[{PUP_BURGUNDY}] text-white"): # Changed cls to _class
                with div(_class="flex justify-around items-center py-3"): # Changed cls to _class
                    with a(href=url_for('home'), _class=f"nav-btn flex flex-col items-center space-y-1 {'opacity-75' if current_nav_item != 'home' else ''}"): # Changed cls to _class
                        i(_class="fas fa-home text-xl") # Changed cls to _class
                        span("Home", _class="text-xs") # Changed cls to _class
                    with a(href=url_for('cart'), _class=f"nav-btn flex flex-col items-center space-y-1 relative {'opacity-75' if current_nav_item != 'cart' else ''}"): # Changed cls to _class
                        i(_class="fas fa-shopping-cart text-xl") # Changed cls to _class
                        span("Cart", _class="text-xs") # Changed cls to _class
                        total_cart_items = sum(session.get('cart', {}).values())
                        if total_cart_items > 0:
                            span(str(total_cart_items), id="nav-cart-badge", _class="cart-badge") # Changed cls to _class
                        else:
                            span(str(total_cart_items), id="nav-cart-badge", _class="cart-badge", style="display: none;") # Changed cls to _class
                    with a(href=url_for('profile'), _class=f"nav-btn flex flex-col items-center space-y-1 {'opacity-75' if current_nav_item != 'profile' else ''}"): # Changed cls to _class
                        i(_class="fas fa-user text-xl") # Changed cls to _class
                        span("Profile", _class="text-xs") # Changed cls to _class
        
        # Help Button (fixed position, from example)
        if show_header_nav:
            a(href=url_for('contact_us'), _class="fixed bottom-24 right-4 w-12 h-12 bg-black text-white rounded-full shadow-lg z-40 flex items-center justify-center"): # Changed cls to _class
                i(_class="fas fa-question") # Changed cls to _class

    return doc.render()

# --- Page Content Generators (Adapted to Tailwind CSS) ---

# Login Section (matches example's login section)
def login_content(_):
    with div(_class="text-center mb-6"): # Changed cls to _class
        with div(_class=f"w-16 h-16 bg-[{PUP_GOLD}] rounded-full flex items-center justify-center mx-auto mb-4"): # Changed cls to _class
            i(_class="fas fa-star text-red-800 text-2xl") # Changed cls to _class
        h2("Welcome Back", _class=f"text-2xl font-bold text-[{PUP_BURGUNDY}]") # Changed cls to _class

    with form(action=url_for('login'), method="post", _class="bg-white rounded-lg shadow-lg p-6"): # Changed cls to _class
        with div(_class="mb-4"): # Changed cls to _class
            label("Email Address:", _class="block text-gray-700 font-semibold mb-2", _for="email") # Changed cls to _class
            input_(type="email", name="email", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500") # Changed cls to _class
        with div(_class="mb-6"): # Changed cls to _class
            label("Password:", _class="block text-gray-700 font-semibold mb-2", _for="password") # Changed cls to _class
            input_(type="password", name="password", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500") # Changed cls to _class

        with div(_class="space-y-3"): # Changed cls to _class
            button("LOGIN", type="submit", _class=f"w-full bg-[{PUP_BURGUNDY}] text-white py-3 rounded-lg font-semibold hover:bg-[{PUP_DARK_BURGUNDY}] transition-colors") # Changed cls to _class
            a("Create Account", href=url_for('register_page'), _class=f"w-full bg-[{PUP_TEAL}] text-white py-3 rounded-lg font-semibold hover:bg-cyan-500 transition-colors flex items-center justify-center") # Changed cls to _class

# Registration Section (matches Image 1 exactly, with Tailwind)
def registration_content(_):
    with div(_class="text-center mb-6"): # Changed cls to _class
        with div(_class=f"w-16 h-16 bg-[{PUP_GOLD}] rounded-full flex items-center justify-center mx-auto mb-4"): # Changed cls to _class
            i(_class="fas fa-star text-red-800 text-2xl") # Changed cls to _class
        h2("Mula sayo para sa bayan", _class=f"text-2xl font-bold text-[{PUP_BURGUNDY}]") # Changed cls to _class

    with form(action=url_for('handle_register'), method="post", _class="bg-white rounded-lg shadow-lg p-6"): # Changed cls to _class
        with div(_class="mb-4"): # Changed cls to _class
            label("Name:", _class="block text-gray-700 font-semibold mb-2", _for="name") # Changed cls to _class
            input_(type="text", name="name", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500") # Changed cls to _class
        with div(_class="mb-4"): # Changed cls to _class
            label("Email Address:", _class="block text-gray-700 font-semibold mb-2", _for="email") # Changed cls to _class
            input_(type="email", name="email", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500") # Changed cls to _class
        with div(_class="mb-4"): # Changed cls to _class
            label("Password:", _class="block text-gray-700 font-semibold mb-2", _for="password") # Changed cls to _class
            input_(type="password", name="password", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500") # Changed cls to _class
        with div(_class="mb-6"): # Changed cls to _class
            label("Confirm Password:", _class="block text-gray-700 font-semibold mb-2", _for="confirm_password") # Changed cls to _class
            input_(type="password", name="confirm_password", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500") # Changed cls to _class

        with div(_class="space-y-3"): # Changed cls to _class
            # The "Back to LOGIN" button from image 1 is actually a link styled as a button
            a("Back to LOGIN", href=url_for('login_page'), _class=f"w-full bg-[{PUP_TEAL}] text-white py-3 rounded-lg font-semibold hover:bg-cyan-500 transition-colors flex items-center justify-center") # Changed cls to _class
            button("REGISTER", type="submit", _class=f"w-full bg-[{PUP_TEAL}] text-white py-3 rounded-lg font-semibold hover:bg-cyan-600 transition-colors") # Changed cls to _class
    
    # Question Mark button (as per image 1)
    a(href=url_for('contact_us'), _class="fixed bottom-4 right-4 w-12 h-12 bg-black text-white rounded-full shadow-lg z-40 flex items-center justify-center"): # Changed cls to _class
        i(_class="fas fa-question text-xl") # Changed cls to _class


# Homepage/Product Listing Section (matches example's homepage)
def homepage_content(_):
    with div(_class="mb-6"): # Changed cls to _class
        h2("Featured Products", _class=f"text-2xl font-bold text-[{PUP_BURGUNDY}] mb-2") # Changed cls to _class
        p("Official PUP merchandise and study essentials", _class="text-gray-600") # Changed cls to _class

    # Featured Product (from example)
    with div(_class="bg-white rounded-lg shadow-lg p-4 mb-6"): # Changed cls to _class
        with div(_class="flex items-start space-x-4"): # Changed cls to _class
            # Placeholder for product image. Replace with actual image.
            img(src="/static/images/product_lanyard_1.png", _class=f"w-24 h-24 bg-[{PUP_BURGUNDY}] rounded-lg object-cover") # Changed cls to _class
            with div(_class="flex-1"): # Changed cls to _class
                h3("PUP STUDY WITH STYLE Baybayin - Classic Edition", _class=f"font-bold text-[{PUP_BURGUNDY}] text-lg") # Changed cls to _class
                p("Polytechnic University (PUP) Lanyard", _class="text-sm text-gray-600 mb-2") # Changed cls to _class
                with div(_class="flex items-center justify-between"): # Changed cls to _class
                    span("₱140", _class=f"text-2xl font-bold text-[{PUP_BURGUNDY}]") # Changed cls to _class
                    with form(action=url_for('add_to_cart'), method="post", style="display:inline;"):
                        input_(type="hidden", name="product_id", value="1") # Assuming ID 1 for this lanyard
                        button("ADD TO CART", type="submit", _class="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-full font-bold transition-colors") # Changed cls to _class

    # You Might Like Section (from example, using actual products from DB)
    with div(_class="mb-6"): # Changed cls to _class
        h3("You Might Like", _class=f"text-xl font-bold text-[{PUP_BURGUNDY}] mb-4") # Changed cls to _class
        with div(_class="grid grid-cols-1 gap-4"): # Changed cls to _class
            products = db.get_all_products() # Get all products for "You Might Like"
            for product in products:
                if product['id'] == 1: continue # Skip the featured product if it's there
                with div(_class="bg-white rounded-lg shadow-md p-4 product-card"): # Changed cls to _class
                    with div(_class="flex items-center space-x-4"): # Changed cls to _class
                        img(src=product['image_url'], _class=f"w-16 h-16 bg-[{PUP_BURGUNDY}] rounded-lg flex items-center justify-center text-white object-cover") # Changed cls to _class
                        with div(_class="flex-1"): # Changed cls to _class
                            h4(product['name'], _class=f"font-semibold text-[{PUP_BURGUNDY}]") # Changed cls to _class
                            p(product['description'], _class="text-sm text-gray-600") # Changed cls to _class
                            with div(_class="flex justify-between items-center mt-2"): # Changed cls to _class
                                span(f"₱{product['price']:.2f}", _class=f"font-bold text-[{PUP_BURGUNDY}]") # Changed cls to _class
                                with form(action=url_for('add_to_cart'), method="post", style="display:inline;"):
                                    input_(type="hidden", name="product_id", value=str(product['id']))
                                    button("ADD TO CART", type="submit", _class="bg-red-500 text-white px-4 py-1 rounded-full text-sm") # Changed cls to _class

# Product Detail Page (adapted to Tailwind)
def product_detail_content(product):
    if not product:
        h1("Product not found", _class=f"text-2xl font-bold text-[{PUP_BURGUNDY}]") # Changed cls to _class
        return

    with div(_class="bg-white rounded-lg shadow-lg p-4 mb-6"): # Changed cls to _class
        img(src=product['image_url'], _class="w-full max-h-64 object-cover rounded-lg mb-4") # Changed cls to _class
        h1(product['name'], _class=f"text-2xl font-bold text-[{PUP_BURGUNDY}] mb-2") # Changed cls to _class
        h2(f"₱{product['price']:.2f}", _class="text-3xl font-bold text-red-500 mb-2") # Changed cls to _class
        p(f"{product['sold_count']} sold", _class="text-gray-600 text-sm mb-4") # Changed cls to _class
        p(product['description'], _class="text-gray-700 mb-4") # Changed cls to _class

        with div(_class="text-sm text-gray-600 mb-4"): # Changed cls to _class
            p("Guaranteed to get by: 2-3 Days")
            p("✓ Free & Easy Return")
            p("✓ Merchandise Protection")

        if product.get('variations'):
            with div(_class="mb-6"): # Changed cls to _class
                label("Select Variation:", _class="block text-gray-700 font-semibold mb-2") # Changed cls to _class
                select_tag = select(name="variation", _class="w-full p-2 border border-gray-300 rounded-lg") # Changed cls to _class
                with select_tag:
                    for var in product['variations'].split(','):
                        option(var, value=var)
        
        with div(_class="flex space-x-4"): # Changed cls to _class
            with form(action=url_for('add_to_cart'), method="post", _class="flex-1"): # Changed cls to _class
                input_(type="hidden", name="product_id", value=str(product['id']))
                button("ADD TO CART", type="submit", _class="w-full bg-red-500 hover:bg-red-600 text-white py-3 rounded-lg font-bold transition-colors") # Changed cls to _class
            with form(action=url_for('add_to_cart'), method="post", _class="flex-1"): # Changed cls to _class
                input_(type="hidden", name="product_id", value=str(product['id']))
                button("BUY NOW", type="submit", _class=f"w-full bg-[{PUP_BURGUNDY}] hover:bg-[{PUP_DARK_BURGUNDY}] text-white py-3 rounded-lg font-bold transition-colors") # Changed cls to _class

# Shopping Cart Section (fully functional with Tailwind)
def cart_content(_):
    h2("Shopping Cart", _class=f"text-2xl font-bold text-[{PUP_BURGUNDY}] mb-4") # Changed cls to _class
    
    with div(_class=f"bg-gradient-to-r from-[{PUP_GOLD}] to-orange-400 rounded-lg p-4 mb-6"): # Changed cls to _class
        with div(_class="text-center"): # Changed cls to _class
            h3("POLYTECHNIC UNIVERSITY OF THE PHILIPPINES", _class="font-bold text-white text-lg mb-2") # Changed cls to _class
            with div(_class="bg-white bg-opacity-20 rounded p-2 inline-block"): # Changed cls to _class
                i(_class="fas fa-university text-white text-2xl") # Changed cls to _class

    cart_items = session.get('cart', {})
    total_price = 0

    with div(id="cart-items", _class="space-y-4 mb-6"): # Changed cls to _class
        if not cart_items:
            with div(_class="text-center text-gray-500 py-8"): # Changed cls to _class
                i(_class="fas fa-shopping-cart text-4xl mb-4") # Changed cls to _class
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
                    with div(_class="bg-white rounded-lg shadow-md p-4"): # Changed cls to _class
                        with div(_class="flex items-center justify-between"): # Changed cls to _class
                            with div(_class="flex items-center space-x-3"): # Changed cls to _class
                                input_(type="checkbox", checked=True, _class="w-4 h-4 text-red-500") # Changed cls to _class
                                img(src=product['image_url'], _class=f"w-12 h-12 bg-[{PUP_BURGUNDY}] rounded object-cover flex items-center justify-center text-white") # Changed cls to _class
                                with div():
                                    h4(product['name'], _class=f"font-semibold text-[{PUP_BURGUNDY}] text-sm") # Changed cls to _class
                                    p(f"₱{product['price']:.2f}", _class="text-gray-600 text-xs") # Changed cls to _class
                                with div(_class="flex items-center space-x-2"): # Changed cls to _class
                                    a(href=url_for('update_cart_quantity', product_id=product_id, action='decrement'),
                                      _class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center"): # Changed cls to _class
                                        i(_class="fas fa-minus text-xs") # Changed cls to _class
                                    span(str(quantity), _class="w-8 text-center font-semibold") # Changed cls to _class
                                    a(href=url_for('update_cart_quantity', product_id=product_id, action='increment'),
                                      _class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center"): # Changed cls to _class
                                        i(_class="fas fa-plus text-xs") # Changed cls to _class
                                    a(href=url_for('remove_from_cart', product_id=product_id),
                                      _class="text-red-500 hover:text-red-700 ml-2"): # Changed cls to _class
                                        i(_class="fas fa-trash-alt text-base") # Changed cls to _class

    # Cart Summary
    with div(id="cart-summary", _class="bg-white rounded-lg shadow-lg p-4 mb-6" if cart_items else "hidden"): # Changed cls to _class
        with div(_class=f"flex justify-between items-center text-lg font-bold text-[{PUP_BURGUNDY}]"): # Changed cls to _class
            span("Total:")
            span(f"₱{total_price:.2f}", id="cart-total")

    button("CHECK OUT", onclick="alert('Checkout functionality is a work in progress!');",
           _class=f"w-full bg-[{PUP_BURGUNDY}] text-white py-4 rounded-lg font-bold text-lg {'hidden' if not cart_items else ''}") # Changed cls to _class


# Contact Section (matches example's contact section)
def contact_us_content(_):
    with div(_class="text-center mb-6"): # Changed cls to _class
        with div(_class=f"w-16 h-16 bg-[{PUP_GOLD}] rounded-full flex items-center justify-center mx-auto mb-4"): # Changed cls to _class
            i(_class="fas fa-star text-red-800 text-2xl") # Changed cls to _class
        h2("Contact Us", _class=f"text-2xl font-bold text-[{PUP_BURGUNDY}]") # Changed cls to _class

    with form(action=url_for('handle_feedback'), method="post", _class="bg-white rounded-lg shadow-lg p-6"): # Changed cls to _class
        with div(_class="mb-4"): # Changed cls to _class
            label("Name:", _class="block text-gray-700 font-semibold mb-2", _for="name") # Changed cls to _class
            input_(type="text", name="name", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500") # Changed cls to _class
        with div(_class="mb-4"): # Changed cls to _class
            label("Email Address:", _class="block text-gray-700 font-semibold mb-2", _for="email") # Changed cls to _class
            input_(type="email", name="email", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500") # Changed cls to _class
        with div(_class="mb-6"): # Changed cls to _class
            with div(_class="flex items-center mb-2"): # Changed cls to _class
                label("Message", _class="text-gray-700 font-semibold", _for="message") # Changed cls to _class
                i(_class="fas fa-question-circle text-gray-400 ml-2") # Changed cls to _class
            textarea(name="message", rows="4", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500 resize-none") # Changed cls to _class
        button("Submit", type="submit", _class=f"w-full bg-[{PUP_BURGUNDY}] text-white py-3 rounded-lg font-semibold border-2 border-[{PUP_BURGUNDY}] hover:bg-white hover:text-red-800 transition-colors") # Changed cls to _class


# Profile Section (matches example's profile section)
def profile_content(_):
    with div(_class="text-center mb-6"): # Changed cls to _class
        with div(_class="w-20 h-20 bg-gray-300 rounded-full flex items-center justify-center mx-auto mb-4"): # Changed cls to _class
            # Ensure you have assets/images/user_icon.png or change this icon
            # Using img tag instead of i for user_icon.png
            img(src="/static/images/user_icon.png", _class="w-full h-full object-cover rounded-full")
        h2(session.get('user_name', 'Guest'), _class=f"text-2xl font-bold text-[{PUP_BURGUNDY}]") # Changed cls to _class

    with div(_class="bg-white rounded-lg shadow-lg p-6 mb-6"): # Changed cls to _class
        with div(_class="space-y-4"): # Changed cls to _class
            with a(href="#", _class="flex items-center justify-between p-3 border-b hover:bg-gray-50"): # Changed cls to _class
                span("Account Settings", _class="font-semibold") # Changed cls to _class
                i(_class="fas fa-chevron-right text-gray-400") # Changed cls to _class
            with a(href=url_for('order_history'), _class="flex items-center justify-between p-3 border-b hover:bg-gray-50"): # Changed cls to _class
                span("Order History", _class="font-semibold") # Changed cls to _class
                i(_class="fas fa-chevron-right text-gray-400") # Changed cls to _class
            with a(href="#", _class="flex items-center justify-between p-3 border-b hover:bg-gray-50"): # Changed cls to _class
                span("Favorites", _class="font-semibold") # Changed cls to _class
                i(_class="fas fa-chevron-right text-gray-400") # Changed cls to _class
            with a(href=url_for('contact_us'), _class="flex items-center justify-between p-3 hover:bg-gray-50"): # Changed cls to _class
                span("Help & Support", _class="font-semibold") # Changed cls to _class
                i(_class="fas fa-chevron-right text-gray-400") # Changed cls to _class

    with div(_class="space-y-3"): # Changed cls to _class
        # Display Sign Out button if logged in
        if 'user_id' in session:
            a("Sign Out", href=url_for('logout'), _class=f"w-full bg-[{PUP_BURGUNDY}] text-white py-3 rounded-lg font-semibold flex items-center justify-center") # Changed cls to _class
        else:
            # Otherwise, display Sign In and Create Account buttons
            a("Sign In", href=url_for('login_page'), _class=f"w-full bg-[{PUP_BURGUNDY}] text-white py-3 rounded-lg font-semibold flex items-center justify-center") # Changed cls to _class
            a("Create Account", href=url_for('register_page'), _class="w-full bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold flex items-center justify-center") # Changed cls to _class

# Order History Section (adapted to Tailwind)
def order_history_content(_):
    h1("Order History", _class=f"text-2xl font-bold text-[{PUP_BURGUNDY}] mb-4") # Changed cls to _class
    
    with div(_class="bg-white rounded-lg shadow-lg p-6"): # Changed cls to _class
        with table(_class="min-w-full divide-y divide-gray-200"): # Changed cls to _class
            with thead(_class=f"bg-[{PUP_BURGUNDY}]"): # Changed cls to _class
                with tr():
                    th("Ref No.", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider") # Changed cls to _class
                    th("Order Status", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider") # Changed cls to _class
                    th("Quantity", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider") # Changed cls to _class
                    th("Payment", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider") # Changed cls to _class
            with tbody(_class="bg-white divide-y divide-gray-200"): # Changed cls to _class
                with tr():
                    td("ORD-20250613-001", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-900") # Changed cls to _class
                    td("Delivered", _class="px-4 py-2 whitespace-nowrap text-sm text-green-600 font-semibold") # Changed cls to _class
                    td("2 items", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500") # Changed cls to _class
                    td("₱320.00 (COD)", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500") # Changed cls to _class
                with tr():
                    td("ORD-20250610-002", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-900") # Changed cls to _class
                    td("Processing", _class="px-4 py-2 whitespace-nowrap text-sm text-blue-600 font-semibold") # Changed cls to _class
                    td("1 item", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500") # Changed cls to _class
                    td("₱450.00 (COD)", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500") # Changed cls to _class
                with tr():
                    td("ORD-20250605-003", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-900") # Changed cls to _class
                    td("Cancelled", _class="px-4 py-2 whitespace-nowrap text-sm text-red-600 font-semibold") # Changed cls to _class
                    td("3 items", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500") # Changed cls to _class
                    td("₱600.00 (COD)", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500") # Changed cls to _class

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