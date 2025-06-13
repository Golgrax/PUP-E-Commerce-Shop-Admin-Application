from flask import Flask, send_from_directory, render_template_string, request, redirect, url_for
import dominate
from dominate.tags import *
from shared import database as db

# --- Flask App Initialization ---
app = Flask(__name__, static_folder='../assets')

# Base page structure to avoid repetition
def create_base_page(page_title, content_div):
    doc = dominate.document(title=page_title)
    with doc.head:
        meta(charset="UTF-8")
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        link(rel="stylesheet", href="/static/css/style.css")
    
    with doc.body:
        with div(cls="container"):
            content_div(app) # Pass app context if needed for url_for
    return doc.render()

# --- Page Content Generators ---
def login_register_content(_):
    img(src="/static/images/pup_logo.png", cls="logo")
    h1("Mula sayo para sa bayan", style="color: #8c1515;")
    
    with form(action="/register", method="post"):
        h2("Register")
        label("Name:", _for="name")
        input_(type="text", id="name", name="name", required=True)
        label("Email Address:", _for="email")
        input_(type="email", id="email", name="email", required=True)
        label("Password:", _for="password")
        input_(type="password", id="password", name="password", required=True)
        # In a real app, confirm password would be validated
        label("Confirm Password:", _for="confirm_password")
        input_(type="password", id="confirm_password", name="confirm_password", required=True)
        button("REGISTER", type="submit", cls="btn-secondary")
    
    # Simple separator
    hr()
    a("Already have an account? Login (Feature WIP)", href="#")


def homepage_content(_):
    img(src="/static/images/pup_logo.png", cls="logo")
    h1("Homepage")
    h2("Best Sellers")

    products = db.get_all_products()
    with div(cls="product-grid"):
        for p in products:
            with a(href=url_for('product_detail', product_id=p['id']), cls="product-item"):
                img(src=p['image_url'])
                h3(p['name'])
                p(f"₱{p['price']:.2f}")

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

    with form(action="/add-to-cart", method="post"):
        input_(type="hidden", name="product_id", value=product['id'])
        # Placeholder for variations
        if product.get('variations'):
            label("Select Variation:")
            select_tag = select(name="variation")
            with select_tag:
                for var in product['variations'].split(','):
                    option(var, value=var)
        
        button("ADD TO CART", type="submit", cls="btn-primary")
        button("BUY NOW", type="submit", cls="btn-secondary") # For simplicity, also adds to cart

# Other page content generators (cart, profile, etc.) would go here...

def cart_content(_):
    h1("Shopping Cart")
    # This is a simplified version. A real cart needs user sessions.
    # For now, it's just a placeholder page.
    div("Your cart is currently empty.")
    p("Add items from the homepage to see them here.")
    a("CHECK OUT", href="#", cls="btn btn-checkout")

def profile_content(_):
    h1("User Profile")
    div(cls="profile-section")
    p("Address 1: (Placeholder)")
    p("Address 2: (Placeholder)")
    
    a("Order History", href=url_for('order_history'))
    br()
    a("Contact Us", href=url_for('contact_us'))
    br()
    a("Logout (WIP)", href="#")

def order_history_content(_):
    h1("Order History")
    # Placeholder data
    with table(cls="admin-table"):
        with thead():
            with tr():
                th("Ref No.")
                th("Order Status")
                th("Quantity")
                th("Payment")
        with tbody():
            with tr():
                td("ORD-123")
                td("Delivered")
                td("2")
                td("₱320.00")

def contact_us_content(_):
    h1("Contact Us")
    with form(action="/submit-feedback", method="post"):
        label("Name:")
        input_(type="text", name="name")
        label("Email Address:")
        input_(type="email", name="email")
        label("Message:")
        textarea(name="message", rows="5")
        button("Submit", type="submit", cls="btn-primary")

# --- Flask Routes ---
@app.route('/')
def login_register_page():
    return create_base_page("Welcome", login_register_content)

@app.route('/home')
def home():
    return create_base_page("Homepage", homepage_content)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = db.get_product_by_id(product_id)
    return create_base_page(product['name'] if product else "Not Found", lambda _: product_detail_content(product))

@app.route('/cart')
def cart():
    return create_base_page("Shopping Cart", cart_content)

@app.route('/profile')
def profile():
    return create_base_page("Profile", profile_content)

@app.route('/order-history')
def order_history():
    return create_base_page("Order History", order_history_content)
    
@app.route('/contact')
def contact_us():
    return create_base_page("Contact Us", contact_us_content)

# --- Form Handling Routes ---
@app.route('/register', methods=['POST'])
def handle_register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    # Add validation here in a real app
    db.create_user(name, email, password)
    # Redirect to home, ideally with a success message
    return redirect(url_for('home'))

@app.route('/submit-feedback', methods=['POST'])
def handle_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    print(f"Feedback Received:\nName: {name}\nEmail: {email}\nMessage: {message}")
    # Redirect back to home with a thank you message (simplified)
    return redirect(url_for('home'))

# Other form handlers (add to cart, etc.) would go here.
@app.route('/add-to-cart', methods=['POST'])
def handle_add_to_cart():
    product_id = request.form.get('product_id')
    print(f"Product {product_id} added to cart! (Functionality is a placeholder)")
    return redirect(url_for('cart'))