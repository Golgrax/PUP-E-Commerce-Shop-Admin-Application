# admin_app/admin_pages.py

import os
from flask import Flask, request, redirect, url_for
import dominate
from dominate.tags import *
from shared import database as db

# --- Admin Flask App Initialization ---
static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
app = Flask(__name__, static_folder=static_folder_path, static_url_path='/static')

# Constants for PUP Colors
PUP_BURGUNDY = '#722F37'
PUP_GOLD = '#FFD700'

def create_admin_page(page_title, content_func):
    doc = dominate.document(title=f"PUP Admin - {page_title}")
    with doc.head:
        link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css")
        link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css")
        link(rel="stylesheet", href="/static/css/style.css") # For custom font and variables
    with doc.body(cls="bg-gray-50 font-sans"):
        with div(cls="container mx-auto p-4 max-w-4xl"):
            # Admin Header
            with header(cls=f"bg-[{PUP_BURGUNDY}] text-white p-4 shadow-lg flex items-center justify-between mb-6"):
                with div(cls="flex items-center space-x-3"):
                    with div(cls=f"w-8 h-8 bg-[{PUP_GOLD}] rounded-full flex items-center justify-center"):
                        i(cls="fas fa-tools text-red-800")
                    h1(page_title, cls="text-xl font-bold")
                with nav():
                    ul(
                        li(a("Inventory", href=url_for('admin_dashboard'), cls="text-white hover:text-gray-200 mx-2")),
                        li(a("Orders (WIP)", href="#", cls="text-white hover:text-gray-200 mx-2")),
                        cls="flex"
                    )

            # Main content
            content_func()
    return doc.render()

def inventory_management_content():
    h2("Inventory Management", cls=f"text-2xl font-bold text-[{PUP_BURGUNDY}] mb-4")
    
    # Form for CRUD operations
    with form(action=url_for('handle_admin_action'), method="post", cls="bg-white rounded-lg shadow-lg p-6 mb-6"):
        with div(cls="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4"):
            with div():
                label("Item ID (for Update/Delete):", cls="block text-gray-700 font-semibold mb-2", _for="item_id")
                input_(type="text", name="item_id", id="item_id", placeholder="e.g., 1", cls="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500")
            with div():
                label("Item Name:", cls="block text-gray-700 font-semibold mb-2", _for="item_name")
                input_(type="text", name="item_name", id="item_name", required=True, cls="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500")
            with div():
                label("Quantity:", cls="block text-gray-700 font-semibold mb-2", _for="quantity")
                input_(type="number", name="quantity", id="quantity", required=True, cls="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500")
            with div():
                label("Price:", cls="block text-gray-700 font-semibold mb-2", _for="price")
                input_(type="text", name="price", id="price", required=True, placeholder="e.g., 150.00", cls="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500")
        
        with div(cls="flex flex-wrap justify-center gap-4"):
            button("Add Item", name="action", value="add", type="submit", cls=f"flex-1 min-w-[120px] bg-[{PUP_BURGUNDY}] text-white py-3 rounded-lg font-semibold hover:bg-[{PUP_DARK_BURGUNDY}] transition-colors")
            button("Update Item", name="action", value="update", type="submit", cls="flex-1 min-w-[120px] bg-blue-500 text-white py-3 rounded-lg font-semibold hover:bg-blue-600 transition-colors")
            button("Delete Item", name="action", value="delete", type="submit", cls="flex-1 min-w-[120px] bg-red-500 text-white py-3 rounded-lg font-semibold hover:bg-red-600 transition-colors")
        
    h2("Current Inventory", cls=f"text-xl font-bold text-[{PUP_BURGUNDY}] mb-4")
    
    products = db.get_all_products()
    with div(cls="overflow-x-auto bg-white rounded-lg shadow-lg"):
        with table(cls="min-w-full divide-y divide-gray-200"):
            with thead(cls=f"bg-[{PUP_BURGUNDY}]"):
                with tr():
                    th("ID", cls="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
                    th("Name", cls="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
                    th("Quantity (Stock)", cls="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
                    th("Price", cls="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
            with tbody(cls="bg-white divide-y divide-gray-200"):
                if not products:
                    with tr():
                        td("No products found.", colspan="4", cls="px-4 py-2 whitespace-nowrap text-sm text-gray-500 text-center")
                for p in products:
                    with tr():
                        td(p['id'], cls="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900")
                        td(p['name'], cls="px-4 py-2 whitespace-nowrap text-sm text-gray-700")
                        td(p['stock'], cls="px-4 py-2 whitespace-nowrap text-sm text-gray-500")
                        td(f"₱{p['price']:.2f}", cls="px-4 py-2 whitespace-nowrap text-sm text-gray-500")

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