# shop_app/web_pages.py

import os
from flask import Flask, request, redirect, url_for, session, flash, get_flashed_messages
import dominate
from dominate.tags import *
from functools import wraps

from shared import database as db

# --- Flask App Initialization ---
static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
app = Flask(__name__, static_folder=static_folder_path, static_url_path='/static')
app.secret_key = 'a-super-secret-key-for-development-change-me' 

# --- CSS Stylesheets (NOW INLINED DIRECTLY IN HTML) ---
# This string will contain ALL the CSS.
# User MUST populate this with content from Tailwind and Font Awesome CDNs.
FULL_INLINE_CSS = """
/*
   -- User Action Required --
   1. Copy the MINIFIED content of https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css
      and paste it here at the beginning of this string.
   2. Copy the MINIFIED content of https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css
      and paste it immediately after the Tailwind CSS content.
   3. Then, paste the custom styles (from your previous style.css) below this comment block.
*/

/* Custom Font */
@font-face {
    font-family: 'RocaOne';
    src: url('/static/fonts/RocaOne-Bold.ttf') format('truetype');
    font-weight: bold;
    font-style: normal;
}

/* Custom CSS variables for PUP colors */
:root {
    --pup-burgundy: #722F37;
    --pup-gold: #FFD700;
    --pup-dark-burgundy: #5A252A;
    --pup-teal-400: #4FD1C5; /* Corresponds to Tailwind cyan-400 */
    --pup-teal-500: #00BCD4; /* Corresponds to Tailwind cyan-500 from your example */
    --pup-red-500: #EF4444; /* Corresponds to Tailwind red-500 */
    --pup-red-600: #DC2626; /* Corresponds to Tailwind red-600 */
    --pup-red-800: #991B1B; /* Corresponds to Tailwind red-800 from your example */
    --pup-red-900: #7F1D1D; /* Corresponds to Tailwind red-900 from your example */
}

/* Custom classes using CSS variables for colors */
.pup-bg-burgundy { background-color: var(--pup-burgundy); }
.pup-bg-gold { background-color: var(--pup-gold); }
.pup-text-burgundy { color: var(--pup-burgundy); }
.pup-text-gold { color: var(--pup-gold); }
.pup-border-burgundy { border-color: var(--pup-burgundy); }

/* Tailwind-like classes for specific colors used in example, now defined in custom CSS */
.bg-yellow-400 { background-color: var(--pup-gold); }
.text-red-800 { color: var(--pup-red-800); }
.bg-red-500 { background-color: var(--pup-red-500); }
.hover\\:bg-red-600:hover { background-color: var(--pup-red-600); } /* Escaped colon for direct class usage */
.bg-cyan-400 { background-color: var(--pup-teal-400); }
.hover\\:bg-cyan-500:hover { background-color: var(--pup-teal-500); } /* Escaped colon */
.bg-cyan-500 { background-color: var(--pup-teal-500); }
.hover\\:bg-cyan-600:hover { background-color: #008C99; } /* Escaped colon */
.hover\\:bg-red-900:hover { background-color: var(--pup-red-900); } /* Escaped colon */

/* General Tailwind-like classes from example HTML for consistency */
.flex { display: flex; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.space-x-3 > *:not(:first-child) { margin-left: 0.75rem; } /* Tailwind space-x-3 */
.space-x-4 > *:not(:first-child) { margin-left: 1rem; } /* Tailwind space-x-4 */
.space-y-1 > *:not(:first-child) { margin-top: 0.25rem; } /* Tailwind space-y-1 */
.space-y-3 > *:not(:first-child) { margin-top: 0.75rem; } /* Tailwind space-y-3 */
.space-y-4 > *:not(:first-child) { margin-top: 1rem; } /* Tailwind space-y-4 */
.rounded-full { border-radius: 9999px; }
.rounded-lg { border-radius: 0.5rem; }
.shadow-lg { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
.text-white { color: white; }
.p-4 { padding: 1rem; }
.w-10 { width: 2.5rem; } .h-10 { height: 2.5rem; }
.w-16 { width: 4rem; } .h-16 { height: 4rem; }
.w-20 { width: 5rem; } .h-20 { height: 5rem; }
.w-24 { width: 6rem; } .h-24 { height: 6rem; }
.opacity-90 { opacity: 0.9; }
.text-lg { font-size: 1.125rem; line-height: 1.75rem; }
.text-xl { font-size: 1.25rem; line-height: 1.75rem; }
.text-2xl { font-size: 1.5rem; line-height: 2rem; }
.text-3xl { font-size: 1.875rem; line-height: 2.25rem; }
.text-xs { font-size: 0.75rem; line-height: 1rem; }
.text-sm { font-size: 0.875rem; line-height: 1.25rem; }
.font-bold { font-weight: 700; }
.font-semibold { font-weight: 600; }
.mx-auto { margin-left: auto; margin-right: auto; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-6 { margin-bottom: 1.5rem; }
.py-3 { padding-top: 0.75rem; padding-bottom: 0.75rem; }
.py-4 { padding-top: 1rem; padding-bottom: 1rem; }
.px-4 { padding-left: 1rem; padding-right: 1rem; }
.px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
.border { border-width: 1px; }
.border-gray-300 { border-color: #D1D5DB; } /* Tailwind gray-300 */
.focus\\:outline-none:focus { outline: 2px solid transparent; outline-offset: 2px; } /* Focus outline */
.focus\\:border-red-500:focus { border-color: var(--pup-red-500); } /* Focus border */
.w-full { width: 100%; }
.block { display: block; }
.resize-none { resize: none; }
.object-cover { object-fit: cover; }
.max-h-64 { max-height: 16rem; } /* Tailwind max-h-64 */
.text-gray-500 { color: #6B7280; }
.text-gray-600 { color: #4B5563; }
.text-gray-700 { color: #374151; }
.text-gray-900 { color: #111827; }
.text-red-500 { color: var(--pup-red-500); }
.hover\\:text-red-700:hover { color: #B91C1C; } /* Tailwind red-700 */
.ml-2 { margin-left: 0.5rem; }
.bg-gray-200 { background-color: #E5E7EB; }
.hover\\:bg-gray-300:hover { background-color: #D1D5DB; }
.w-8 { width: 2rem; } .h-8 { height: 2rem; }
.min-w-full { min-width: 100%; }
.divide-y > :not([hidden]) ~ :not([hidden]) { border-top-width: 1px; border-color: #E5E7EB; } /* Tailwind divide-y */
.divide-gray-200 { border-color: #E5E7EB; }
.whitespace-nowrap { white-space: nowrap; }
.uppercase { text-transform: uppercase; }
.tracking-wider { letter-spacing: 0.05em; }
.px-4 { padding-left: 1rem; padding-right: 1rem; }
.py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
.text-left { text-align: left; }
.text-green-600 { color: #16A34A; }
.text-blue-600 { color: #2563EB; }
.text-red-600 { color: var(--pup-red-600); }
.fixed { position: fixed; }
.bottom-0 { bottom: 0; }
.left-0 { left: 0; }
.right-0 { right: 0; }
.bottom-24 { bottom: 6rem; }
.right-4 { right: 1rem; }
.w-12 { width: 3rem; } .h-12 { height: 3rem; }
.bg-black { background-color: #000; }
.shadow-lg { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
.z-40 { z-index: 40; } .z-50 { z-index: 50; }
.relative { position: relative; }
.top-20 { top: 5rem; }

/*
   -- User Action Required --
   End of custom styles.
*/
"""

# --- Login Required Decorator ---
def login_required(f):
    @wraps(f) 
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# --- Base Page Structure (with Inline CSS, Header, and Nav) ---
def create_base_page(page_title, content_func, current_nav_item=None, show_header_nav=True):
    doc = dominate.document(title=f"PUP Mobile Store - {page_title}")
    with doc.head:
        meta(charset="UTF-8")
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        style(FULL_INLINE_CSS) # FIX: Inline all CSS here

    doc.body._class = "bg-gray-50 font-sans"
    with doc.body:
        # Header
        if show_header_nav:
            with header(_class=f"{PUP_BURGUNDY_CLASS} text-white p-4 shadow-lg"):
                with div(_class="flex items-center justify-between"):
                    with div(_class="flex items-center space-x-3"):
                        with div(_class=f"w-10 h-10 {TAILWIND_YELLOW_400} rounded-full flex items-center justify-center"):
                            i(_class=f"fas fa-star {TAILWIND_RED_800}")
                        with div():
                            h1("StudywithStyle", _class="text-lg font-bold")
                            p("PUP Official Store", _class="text-xs opacity-90")
                    with div(_class="flex space-x-3"):
                        with div(_class="relative"):
                            a(href=url_for('cart'), _class="p-2 bg-black bg-opacity-20 rounded-full")(
                                i(_class="fas fa-shopping-cart")
                            )
                            total_cart_items = sum(session.get('cart', {}).values())
                            if total_cart_items > 0:
                                span(str(total_cart_items), id="cart-badge", _class="cart-badge")
                            else:
                                span(str(total_cart_items), id="cart-badge", _class="cart-badge", style="display: none;")
                        a(href=url_for('profile'), _class="p-2 bg-black bg-opacity-20 rounded-full")(
                            i(_class="fas fa-user")
                        )
        
        # Main Content Container
        with main(_class="content-container"):
            # Flash messages
            for category, message in get_flashed_messages(with_categories=True):
                div(message, _class=f"p-3 mb-4 rounded-lg font-semibold text-sm flash-{category}")

            content_func(app)

        # Bottom Navigation
        if show_header_nav:
            with nav(_class=f"bottom-nav {PUP_BURGUNDY_CLASS} text-white"):
                with div(_class="flex justify-around items-center py-3"):
                    with a(href=url_for('home'), _class=f"nav-btn flex flex-col items-center space-y-1 {'opacity-75' if current_nav_item != 'home' else ''}"):
                        i(_class="fas fa-home text-xl")
                        span("Home", _class="text-xs")
                    with a(href=url_for('cart'), _class=f"nav-btn flex flex-col items-center space-y-1 relative {'opacity-75' if current_nav_item != 'cart' else ''}"):
                        i(_class="fas fa-shopping-cart text-xl")
                        span("Cart", _class="text-xs")
                        total_cart_items = sum(session.get('cart', {}).values())
                        if total_cart_items > 0:
                            span(str(total_cart_items), id="nav-cart-badge", _class="cart-badge")
                        else:
                            span(str(total_cart_items), id="nav-cart-badge", _class="cart-badge", style="display: none;")
                    with a(href=url_for('profile'), _class=f"nav-btn flex flex-col items-center space-y-1 {'opacity-75' if current_nav_item != 'profile' else ''}"):
                        i(_class="fas fa-user text-xl")
                        span("Profile", _class="text-xs")
        
        # Help Button
        if show_header_nav:
            a(href=url_for('contact_us'), _class="fixed bottom-24 right-4 w-12 h-12 bg-black text-white rounded-full shadow-lg z-40 flex items-center justify-center")(
                i(_class="fas fa-question")
            )

    return doc.render()

# --- Page Content Generators ---

# Login Section (matches example's login section)
def login_content(_):
    with section(id="login", _class="section p-4"): # Ensure p-4 is on the section
        with div(_class="text-center mb-6"):
            with div(_class=f"w-16 h-16 {TAILWIND_YELLOW_400} rounded-full flex items-center justify-center mx-auto mb-4"):
                i(_class=f"fas fa-star {TAILWIND_RED_800} text-2xl")
            h2("Welcome Back", _class=f"text-2xl font-bold {PUP_TEXT_BURGUNDY_CLASS}")

        with form(action=url_for('login'), method="post", _class="bg-white rounded-lg shadow-lg p-6"):
            with div(_class="mb-4"):
                label("Email Address:", _class="block text-gray-700 font-semibold mb-2", _for="email")
                input_(type="email", name="email", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")
            with div(_class="mb-6"):
                label("Password:", _class="block text-gray-700 font-semibold mb-2", _for="password")
                input_(type="password", name="password", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")

            with div(_class="space-y-3"):
                button("LOGIN", type="submit", _class=f"w-full {PUP_BURGUNDY_CLASS} text-white py-3 rounded-lg font-semibold {TAILWIND_RED_900_HOVER} transition-colors")
                button("Create Account", onclick=f"window.location.href='{url_for('register_page')}'", type="button", _class=f"w-full {TAILWIND_CYAN_400} text-white py-3 rounded-lg font-semibold {TAILWIND_HOVER_CYAN_500} transition-colors")

# Registration Section (matches Image 1 exactly, with custom classes)
def registration_content(_):
    with section(id="register", _class="section p-4"):
        with div(_class="text-center mb-6"):
            with div(_class=f"w-16 h-16 {TAILWIND_YELLOW_400} rounded-full flex items-center justify-center mx-auto mb-4"):
                i(_class=f"fas fa-star {TAILWIND_RED_800} text-2xl")
            h2("Mula sayo para sa bayan", _class=f"text-2xl font-bold {PUP_TEXT_BURGUNDY_CLASS}")

        with form(action=url_for('handle_register'), method="post", _class="bg-white rounded-lg shadow-lg p-6"):
            with div(_class="mb-4"):
                label("Name:", _class="block text-gray-700 font-semibold mb-2", _for="name")
                input_(type="text", name="name", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")
            with div(_class="mb-4"):
                label("Email Address:", _class="block text-gray-700 font-semibold mb-2", _for="email")
                input_(type="email", name="email", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")
            with div(_class="mb-4"):
                label("Password:", _class="block text-gray-700 font-semibold mb-2", _for="password")
                input_(type="password", name="password", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")
            with div(_class="mb-6"):
                label("Confirm Password:", _class="block text-gray-700 font-semibold mb-2", _for="confirm_password")
                input_(type="password", name="confirm_password", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")

            with div(_class="space-y-3"):
                button("Back to LOGIN", onclick=f"window.location.href='{url_for('login_page')}'", type="button", _class=f"w-full {TAILWIND_CYAN_400} text-white py-3 rounded-lg font-semibold {TAILWIND_HOVER_CYAN_500} transition-colors")
                button("REGISTER", type="submit", _class=f"w-full {TAILWIND_CYAN_500} text-white py-3 rounded-lg font-semibold {TAILWIND_HOVER_CYAN_600} transition-colors")
        
        a(href=url_for('contact_us'), _class="fixed bottom-4 right-4 w-12 h-12 bg-black text-white rounded-full shadow-lg z-40 flex items-center justify-center")(
            i(_class="fas fa-question text-xl")
        )


# Homepage/Product Listing Section (matches example's homepage)
def homepage_content(_):
    with section(id="homepage", _class="section active p-4"):
        with div(_class="mb-6"):
            h2("Featured Products", _class=f"text-2xl font-bold {PUP_TEXT_BURGUNDY_CLASS} mb-2")
            p("Official PUP merchandise and study essentials", _class="text-gray-600")

        with div(_class="bg-white rounded-lg shadow-lg p-4 mb-6"):
            with div(_class="flex items-start space-x-4"):
                img(src="/static/images/product_lanyard_1.png", _class=f"w-24 h-24 {PUP_BURGUNDY_CLASS} rounded-lg object-cover")
                with div(_class="flex-1"):
                    h3("PUP STUDY WITH STYLE Baybayin - Classic Edition", _class=f"font-bold {PUP_TEXT_BURGUNDY_CLASS} text-lg")
                    p("Polytechnic University (PUP) Lanyard", _class="text-sm text-gray-600 mb-2")
                    with div(_class="flex items-center justify-between"):
                        span("₱140", _class=f"text-2xl font-bold {PUP_TEXT_BURGUNDY_CLASS}")
                        with form(action=url_for('add_to_cart'), method="post", style="display:inline;"):
                            input_(type="hidden", name="product_id", value="1")
                            button("ADD TO CART", type="submit", _class=f"{TAILWIND_RED_500} {TAILWIND_HOVER_RED_600} text-white px-6 py-2 rounded-full font-bold transition-colors")

        with div(_class="mb-6"):
            h3("You Might Like", _class=f"text-xl font-bold {PUP_TEXT_BURGUNDY_CLASS} mb-4")
            with div(_class="grid grid-cols-1 gap-4"):
                products = db.get_all_products()
                for product in products:
                    if product['id'] == 1: continue 
                    
                    with div(_class="bg-white rounded-lg shadow-md p-4 product-card"):
                        with div(_class="flex items-center space-x-4"):
                            img(src=product['image_url'], _class=f"w-16 h-16 {PUP_BURGUNDY_CLASS} rounded-lg flex items-center justify-center text-white object-cover")
                            with div(_class="flex-1"):
                                h4(product['name'], _class=f"font-semibold {PUP_TEXT_BURGUNDY_CLASS}")
                                p(product['description'], _class="text-sm text-gray-600")
                                with div(_class="flex justify-between items-center mt-2"):
                                    span(f"₱{product['price']:.2f}", _class=f"font-bold {PUP_TEXT_BURGUNDY_CLASS}")
                                    with form(action=url_for('add_to_cart'), method="post", style="display:inline;"):
                                        input_(type="hidden", name="product_id", value=str(product['id']))
                                        button("ADD TO CART", type="submit", _class=f"{TAILWIND_RED_500} text-white px-4 py-1 rounded-full text-sm")

# Product Detail Page (adapted to Tailwind)
def product_detail_content(product):
    with section(id="product-detail", _class="section p-4"):
        if not product:
            h1("Product not found", _class=f"text-2xl font-bold {PUP_TEXT_BURGUNDY_CLASS}")
            return

        with div(_class="bg-white rounded-lg shadow-lg p-4 mb-6"):
            img(src=product['image_url'], _class="w-full max-h-64 object-cover rounded-lg mb-4")
            h1(product['name'], _class=f"text-2xl font-bold {PUP_TEXT_BURGUNDY_CLASS} mb-2")
            h2(f"₱{product['price']:.2f}", _class="text-3xl font-bold text-red-500 mb-2")
            p(f"{product['sold_count']} sold", _class="text-gray-600 text-sm mb-4")
            p(product['description'], _class="text-gray-700 mb-4")

            with div(_class="text-sm text-gray-600 mb-4"):
                p("Guaranteed to get by: 2-3 Days")
                p("✓ Free & Easy Return")
                p("✓ Merchandise Protection")

            if product.get('variations'):
                with div(_class="mb-6"):
                    label("Select Variation:", _class="block text-gray-700 font-semibold mb-2", _for="variation")
                    select_tag = select(name="variation", id="variation", _class="w-full p-2 border border-gray-300 rounded-lg")
                    with select_tag:
                        for var in product['variations'].split(','):
                            option(var, value=var)
            
            with div(_class="flex space-x-4"):
                with form(action=url_for('add_to_cart'), method="post", _class="flex-1"):
                    input_(type="hidden", name="product_id", value=str(product['id']))
                    button("ADD TO CART", type="submit", _class=f"w-full {TAILWIND_RED_500} {TAILWIND_HOVER_RED_600} text-white py-3 rounded-lg font-bold transition-colors")
                with form(action=url_for('add_to_cart'), method="post", _class="flex-1"):
                    input_(type="hidden", name="product_id", value=str(product['id']))
                    button("BUY NOW", type="submit", _class=f"w-full {PUP_BURGUNDY_CLASS} {TAILWIND_RED_900_HOVER} text-white py-3 rounded-lg font-bold transition-colors")


# Shopping Cart Section (fully functional with custom classes)
def cart_content(_):
    with section(id="cart", _class="section p-4"):
        h2("Shopping Cart", _class=f"text-2xl font-bold {PUP_TEXT_BURGUNDY_CLASS} mb-4")
        
        with div(_class=f"bg-gradient-to-r from-yellow-400 to-orange-400 rounded-lg p-4 mb-6"):
            with div(_class="text-center"):
                h3("POLYTECHNIC UNIVERSITY OF THE PHILIPPINES", _class="font-bold text-white text-lg mb-2")
                with div(_class="bg-white bg-opacity-20 rounded p-2 inline-block"):
                    i(_class="fas fa-university text-white text-2xl")

        cart_items = session.get('cart', {})
        total_price = 0

        with div(id="cart-items", _class="space-y-4 mb-6"):
            if not cart_items:
                with div(_class="text-center text-gray-500 py-8"):
                    i(_class="fas fa-shopping-cart text-4xl mb-4")
                    p("Your cart is empty")
            else:
                for product_id_str, quantity in cart_items.items():
                    try:
                        product_id = int(product_id_str)
                    except ValueError:
                        continue
                    
                    product = db.get_product_by_id(product_id)
                    if product:
                        item_total = product['price'] * quantity
                        total_price += item_total
                        with div(_class="bg-white rounded-lg shadow-md p-4"):
                            with div(_class="flex items-center justify-between"):
                                with div(_class="flex items-center space-x-3"):
                                    input_(type="checkbox", checked=True, _class=f"w-4 h-4 text-red-500")
                                    img(src=product['image_url'], _class=f"w-12 h-12 {PUP_BURGUNDY_CLASS} rounded object-cover flex items-center justify-center text-white")
                                    with div():
                                        h4(product['name'], _class=f"font-semibold {PUP_TEXT_BURGUNDY_CLASS} text-sm")
                                        p(f"₱{product['price']:.2f}", _class="text-gray-600 text-xs")
                                with div(_class="flex items-center space-x-2"):
                                    a(href=url_for('update_cart_quantity', product_id=product_id, action='decrement'),
                                      _class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center text-gray-700 hover:bg-gray-300")(
                                        i(_class="fas fa-minus text-xs")
                                    )
                                    span(str(quantity), _class="w-8 text-center font-semibold")
                                    a(href=url_for('update_cart_quantity', product_id=product_id, action='increment'),
                                      _class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center text-gray-700 hover:bg-gray-300")(
                                        i(_class="fas fa-plus text-xs")
                                    )
                                    a(href=url_for('remove_from_cart', product_id=product_id),
                                      _class=f"text-red-500 hover:text-red-700 ml-2")(
                                        i(_class="fas fa-trash-alt text-base")
                                    )

        # Cart Summary
        with div(id="cart-summary", _class="bg-white rounded-lg shadow-lg p-4 mb-6" if cart_items else "hidden"):
            with div(_class=f"flex justify-between items-center text-lg font-bold {PUP_TEXT_BURGUNDY_CLASS}"):
                span("Total:")
                span(f"₱{total_price:.2f}", id="cart-total")

        button("CHECK OUT", onclick="alert('Checkout functionality is a work in progress!');",
           _class=f"w-full {PUP_BURGUNDY_CLASS} text-white py-4 rounded-lg font-bold text-lg {'hidden' if not cart_items else ''}")


# Contact Section (matches example's contact section)
def contact_us_content(_):
    with section(id="contact", _class="section p-4"):
        with div(_class="text-center mb-6"):
            with div(_class=f"w-16 h-16 {TAILWIND_YELLOW_400} rounded-full flex items-center justify-center mx-auto mb-4"):
                i(_class=f"fas fa-star {TAILWIND_RED_800} text-2xl")
            h2("Contact Us", _class=f"text-2xl font-bold {PUP_TEXT_BURGUNDY_CLASS}")

        with form(action=url_for('handle_feedback'), method="post", _class="bg-white rounded-lg shadow-lg p-6"):
            with div(_class="mb-4"):
                label("Name:", _class="block text-gray-700 font-semibold mb-2", _for="name")
                input_(type="text", name="name", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")
            with div(_class="mb-4"):
                label("Email Address:", _class="block text-gray-700 font-semibold mb-2", _for="email")
                input_(type="email", name="email", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500")
            with div(_class="mb-6"):
                with div(_class="flex items-center mb-2"):
                    label("Message", _class="text-gray-700 font-semibold", _for="message")
                    i(_class="fas fa-question-circle text-gray-400 ml-2")
                textarea(name="message", rows="4", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500 resize-none")
            button("Submit", type="submit", _class=f"w-full {PUP_BURGUNDY_CLASS} text-white py-3 rounded-lg font-semibold border-2 {PUP_BORDER_BURGUNDY_CLASS} hover:bg-white hover:text-red-800 transition-colors")


# Profile Section (matches example's profile section)
def profile_content(_):
    with section(id="profile", _class="section p-4"):
        with div(_class="text-center mb-6"):
            with div(_class=f"w-20 h-20 {TAILWIND_GRAY_300} rounded-full flex items-center justify-center mx-auto mb-4"):
                i(_class=f"fas fa-user text-3xl {TAILWIND_GRAY_600}") # Using font awesome icon based on image. if using img, uncomment below line
                #img(src="/static/images/user_icon.png", _class="w-full h-full object-cover rounded-full") # If you prefer image
            h2(session.get('user_name', 'Guest'), _class=f"text-2xl font-bold {PUP_TEXT_BURGUNDY_CLASS}")

        with div(_class="bg-white rounded-lg shadow-lg p-6 mb-6"):
            with div(_class="space-y-4"):
                with a(href="#", _class="flex items-center justify-between p-3 border-b hover:bg-gray-50"):
                    span("Account Settings", _class="font-semibold")
                    i(_class="fas fa-chevron-right text-gray-400")
                with a(href=url_for('order_history'), _class="flex items-center justify-between p-3 border-b hover:bg-gray-50"):
                    span("Order History", _class="font-semibold")
                    i(_class="fas fa-chevron-right text-gray-400")
                with a(href="#", _class="flex items-center justify-between p-3 border-b hover:bg-gray-50"):
                    span("Favorites", _class="font-semibold")
                    i(_class="fas fa-chevron-right text-gray-400")
                with a(href=url_for('contact_us'), _class="flex items-center justify-between p-3 hover:bg-gray-50"):
                    span("Help & Support", _class="font-semibold")
                    i(_class="fas fa-chevron-right text-gray-400")

        with div(_class="space-y-3"):
            if 'user_id' in session:
                a("Sign Out", href=url_for('logout'), _class=f"w-full {PUP_BURGUNDY_CLASS} text-white py-3 rounded-lg font-semibold flex items-center justify-center")
            else:
                a("Sign In", href=url_for('login_page'), _class=f"w-full {PUP_BURGUNDY_CLASS} text-white py-3 rounded-lg font-semibold flex items-center justify-center")
                a("Create Account", href=url_for('register_page'), _class=f"w-full {TAILWIND_GRAY_200} text-gray-700 py-3 rounded-lg font-semibold flex items-center justify-center")


# Order History Section (adapted to Tailwind)
def order_history_content(_):
    with section(id="order-history", _class="section p-4"):
        h1("Order History", _class=f"text-2xl font-bold {PUP_TEXT_BURGUNDY_CLASS} mb-4")
        
        with div(_class="bg-white rounded-lg shadow-lg p-6"):
            with table(_class="min-w-full divide-y divide-gray-200"):
                with thead(_class=PUP_BURGUNDY_CLASS):
                    with tr():
                        th("Ref No.", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
                        th("Order Status", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
                        th("Quantity", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
                        th("Payment", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
                with tbody(_class="bg-white divide-y divide-gray-200"):
                    with tr():
                        td("ORD-20250613-001", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-900")
                        td("Delivered", _class="px-4 py-2 whitespace-nowrap text-sm text-green-600 font-semibold")
                        td("2 items", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500")
                        td("₱320.00 (COD)", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500")
                    with tr():
                        td("ORD-20250610-002", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-900")
                        td("Processing", _class="px-4 py-2 whitespace-nowrap text-sm text-blue-600 font-semibold")
                        td("1 item", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500")
                        td("₱450.00 (COD)", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500")
                    with tr():
                        td("ORD-20250605-003", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-900")
                        td("Cancelled", _class="px-4 py-2 whitespace-nowrap text-sm text-red-600 font-semibold")
                        td("3 items", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500")
                        td("₱600.00 (COD)", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500")

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
    quantity = int(request.form.get('quantity', 1))
    
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
            else:
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