# admin_app/admin_pages.py

import os
from flask import Flask, request, redirect, url_for, flash, get_flashed_messages
import dominate
from dominate.tags import *
from shared import database as db

# --- Admin Flask App Initialization ---
static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
app = Flask(__name__, static_folder=static_folder_path, static_url_path='/static')
app.secret_key = 'another-secret-key-for-admin-app-change-me' # Add a secret key for flash messages

# Constants for PUP Colors
PUP_BURGUNDY = '#722F37'
PUP_GOLD = '#FFD700'
PUP_DARK_BURGUNDY = '#5A252A'

def create_admin_page(page_title, content_func):
    doc = dominate.document(title=f"PUP Admin - {page_title}")
    with doc.head:
        link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css")
        link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css")
        link(rel="stylesheet", href="/static/css/style.css") # For custom font and variables
    with doc.body(_class="bg-gray-50 font-sans"): # Changed cls to _class
        with div(_class="container mx-auto p-4 max-w-4xl"): # Changed cls to _class
            # Admin Header
            with header(_class=f"bg-[{PUP_BURGUNDY}] text-white p-4 shadow-lg flex items-center justify-between mb-6"): # Changed cls to _class
                with div(_class="flex items-center space-x-3"): # Changed cls to _class
                    with div(_class=f"w-8 h-8 bg-[{PUP_GOLD}] rounded-full flex items-center justify-center"): # Changed cls to _class
                        i(_class="fas fa-tools text-red-800") # Changed cls to _class
                    h1(page_title, _class="text-xl font-bold") # Changed cls to _class
                with nav():
                    ul(
                        li(a("Inventory", href=url_for('admin_dashboard'), _class="text-white hover:text-gray-200 mx-2")), # Changed cls to _class
                        li(a("Orders (WIP)", href="#", _class="text-white hover:text-gray-200 mx-2")), # Changed cls to _class
                        _class="flex" # Changed cls to _class
                    )

            # Flash messages (style them with Tailwind using .flash-success, .flash-error)
            for category, message in get_flashed_messages(with_categories=True):
                div(message, _class=f"p-3 mb-4 rounded-lg font-semibold text-sm flash-{category}") # Changed cls to _class

            # Main content
            content_func()
    return doc.render()

def inventory_management_content():
    h2("Inventory Management", _class=f"text-2xl font-bold text-[{PUP_BURGUNDY}] mb-4") # Changed cls to _class
    
    # Form for CRUD operations
    with form(action=url_for('handle_admin_action'), method="post", _class="bg-white rounded-lg shadow-lg p-6 mb-6"): # Changed cls to _class
        with div(_class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4"): # Changed cls to _class
            with div():
                label("Item ID (for Update/Delete):", _class="block text-gray-700 font-semibold mb-2", _for="item_id") # Changed cls to _class
                input_(type="text", name="item_id", id="item_id", placeholder="e.g., 1", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500") # Changed cls to _class
            with div():
                label("Item Name:", _class="block text-gray-700 font-semibold mb-2", _for="item_name") # Changed cls to _class
                input_(type="text", name="item_name", id="item_name", required=True, _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500") # Changed cls to _class
            with div():
                label("Quantity:", _class="block text-gray-700 font-semibold mb-2", _for="quantity") # Changed cls to _class
                input_(type="number", name="quantity", id="quantity", required=True, _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500") # Changed cls to _class
            with div():
                label("Price:", _class="block text-gray-700 font-semibold mb-2", _for="price") # Changed cls to _class
                input_(type="text", name="price", id="price", required=True, placeholder="e.g., 150.00", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500") # Changed cls to _class
        
        with div(_class="flex flex-wrap justify-center gap-4"): # Changed cls to _class
            button("Add Item", name="action", value="add", type="submit", _class=f"flex-1 min-w-[120px] bg-[{PUP_BURGUNDY}] text-white py-3 rounded-lg font-semibold hover:bg-[{PUP_DARK_BURGUNDY}] transition-colors") # Changed cls to _class
            button("Update Item", name="action", value="update", type="submit", _class="flex-1 min-w-[120px] bg-blue-500 text-white py-3 rounded-lg font-semibold hover:bg-blue-600 transition-colors") # Changed cls to _class
            button("Delete Item", name="action", value="delete", type="submit", _class="flex-1 min-w-[120px] bg-red-500 text-white py-3 rounded-lg font-semibold hover:bg-red-600 transition-colors") # Changed cls to _class
        
    h2("Current Inventory", _class=f"text-xl font-bold text-[{PUP_BURGUNDY}] mb-4") # Changed cls to _class
    
    products = db.get_all_products()
    with div(_class="overflow-x-auto bg-white rounded-lg shadow-lg"): # Changed cls to _class
        with table(_class="min-w-full divide-y divide-gray-200"): # Changed cls to _class
            with thead(_class=f"bg-[{PUP_BURGUNDY}]"): # Changed cls to _class
                with tr():
                    th("ID", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider") # Changed cls to _class
                    th("Name", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider") # Changed cls to _class
                    th("Quantity (Stock)", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider") # Changed cls to _class
                    th("Price", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider") # Changed cls to _class
            with tbody(_class="bg-white divide-y divide-gray-200"): # Changed cls to _class
                if not products:
                    with tr():
                        td("No products found.", colspan="4", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500 text-center") # Changed cls to _class
                for p in products:
                    with tr():
                        td(p['id'], _class="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900") # Changed cls to _class
                        td(p['name'], _class="px-4 py-2 whitespace-nowrap text-sm text-gray-700") # Changed cls to _class
                        td(p['stock'], _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500") # Changed cls to _class
                        td(f"₱{p['price']:.2f}", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500") # Changed cls to _class

@app.route('/admin')
def admin_dashboard():
    return create_admin_page("Inventory Management", inventory_management_content)

@app.route('/admin/action', methods=['POST'])
def handle_admin_action():
    action = request.form.get('action')
    item_id = request.form.get('item_id')
    item_name = request.form.get('item_name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')

    # Basic validation
    if action in ['add', 'update'] and (not item_name or not quantity or not price):
        flash("Name, Quantity, and Price are required for Add/Update.", 'error')
        return redirect(url_for('admin_dashboard'))
    if action in ['update', 'delete'] and not item_id:
        flash("Item ID is required for Update/Delete.", 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        if item_id: item_id = int(item_id)
        if quantity: quantity = int(quantity)
        if price: price = float(price)
    except ValueError:
        flash("Quantity and Price must be numbers, Item ID must be an integer.", 'error')
        return redirect(url_for('admin_dashboard'))

    if action == 'add':
        if db.add_product(item_name, quantity, price):
            flash("Product added successfully!", 'success')
        else:
            flash("Failed to add product.", 'error')
    elif action == 'update':
        if db.update_product(item_id, item_name, quantity, price):
            flash("Product updated successfully!", 'success')
        else:
            flash("Failed to update product.", 'error')
    elif action == 'delete':
        if db.delete_product(item_id):
            flash("Product deleted successfully!", 'success')
        else:
            flash("Failed to delete product.", 'error')
            
    return redirect(url_for('admin_dashboard'))