# admin_app/admin_pages.py

import os  # <-- Make sure os is imported
from flask import Flask, request, redirect, url_for
import dominate
from dominate.tags import *
from shared import database as db

# --- Admin Flask App Initialization (CORRECTED AND FINAL) ---
# Create an absolute path from this file's location to the parent directory's 'assets' folder
static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
app = Flask(__name__, static_folder=static_folder_path, static_url_path='/static')


def create_admin_page(page_title, content_func):
    doc = dominate.document(title=page_title)
    with doc.head:
        link(rel="stylesheet", href="/static/css/style.css")
    with doc.body:
        with div(cls="container", style="max-width: 750px;"):
            content_func()
    return doc.render()

def inventory_management_content():
    h1("Inventory Management")
    
    with form(action="/admin/action", method="post"):
        with table(style="width: 100%; text-align: left;"):
            with tr():
                td(label("Item ID (for Update/Delete):"))
                td(input_(type="text", name="item_id", placeholder="e.g., 1"))
            with tr():
                td(label("Item Name:"))
                td(input_(type="text", name="item_name", required=True))
            with tr():
                td(label("Quantity:"))
                td(input_(type="number", name="quantity", required=True))
            with tr():
                td(label("Price:"))
                td(input_(type="text", name="price", required=True, placeholder="e.g., 150.00"))
        
        button("Add Item", name="action", value="add", type="submit", cls="btn-primary")
        button("Update Item", name="action", value="update", type="submit", cls="btn-secondary")
        button("Delete Item", name="action", value="delete", type="submit", cls="btn-danger", style="background-color: #f44336;")
        
    hr()
    h2("Current Inventory")
    
    products = db.get_all_products()
    with table(cls="admin-table"):
        with thead():
            with tr():
                th("ID")
                th("Name")
                th("Quantity (Stock)")
                th("Price")
        with tbody():
            if not products:
                with tr():
                    td("No products found.", colspan="4")
            for p in products:
                with tr():
                    td(p['id'])
                    td(p['name'])
                    td(p['stock'])
                    td(f"₱{p['price']:.2f}")

@app.route('/admin')
def admin_dashboard():
    return create_admin_page("Admin - Inventory", inventory_management_content)

@app.route('/admin/action', methods=['POST'])
def handle_admin_action():
    action = request.form.get('action')
    item_id = request.form.get('item_id')
    item_name = request.form.get('item_name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')

    if action == 'add':
        if item_name and quantity and price:
            db.add_product(item_name, int(quantity), float(price))
    elif action == 'update':
        if item_id and item_name and quantity and price:
            db.update_product(int(item_id), item_name, int(quantity), float(price))
    elif action == 'delete':
        if item_id:
            db.delete_product(int(item_id))
            
    return redirect(url_for('admin_dashboard'))