# admin_app/admin_pages.py

import os
from flask import Flask, request, redirect, url_for, flash, get_flashed_messages
import dominate
from dominate.tags import *
from shared import database as db

# --- Admin Flask App Initialization ---
static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
app = Flask(__name__, static_folder=static_folder_path, static_url_path='/static')
app.secret_key = 'another-secret-key-for-admin-app-change-me' 

# --- CSS Stylesheets (NOW INLINED DIRECTLY IN HTML) ---
# This string will contain ALL the CSS.
# User MUST populate this with content from Tailwind and Font Awesome CDNs.
FULL_INLINE_CSS_ADMIN = """
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
    --pup-red-800: #991B1B;
    --pup-red-900: #7F1D1D;
}

/* Custom classes using CSS variables for colors */
.pup-bg-burgundy { background-color: var(--pup-burgundy); }
.pup-bg-gold { background-color: var(--pup-gold); }
.pup-text-burgundy { color: var(--pup-burgundy); }

/* Tailwind-like classes for specific colors used in example, now defined in custom CSS */
.text-red-800 { color: var(--pup-red-800); }
.hover\\:bg-red-900:hover { background-color: var(--pup-red-900); } /* Escaped colon */

/* General Tailwind-like classes for consistency */
.flex { display: flex; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.space-x-3 > *:not(:first-child) { margin-left: 0.75rem; }
.mx-auto { margin-left: auto; margin-right: auto; }
.p-4 { padding: 1rem; }
.mb-6 { margin-bottom: 1.5rem; }
.text-white { color: white; }
.shadow-lg { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
.w-8 { width: 2rem; } .h-8 { height: 2rem; }
.rounded-full { border-radius: 9999px; }
.text-xl { font-size: 1.25rem; line-height: 1.75rem; }
.font-bold { font-weight: 700; }
.hover\\:text-gray-200:hover { color: #E5E7EB; } /* Escaped colon */
.mx-2 { margin-left: 0.5rem; margin-right: 0.5rem; }
.container { width: 100%; } /* Max-width handled by default Tailwind */
.max-w-4xl { max-width: 56rem; } /* Tailwind max-w-4xl */
.text-2xl { font-size: 1.5rem; line-height: 2rem; }
.mb-4 { margin-bottom: 1rem; }
.bg-white { background-color: #fff; }
.rounded-lg { border-radius: 0.5rem; }
.p-6 { padding: 1.5rem; }
.gap-4 { gap: 1rem; }
.grid { display: grid; }
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.md\\:grid-cols-2 { /* Media query for md screen, Tkhtml is not responsive, so this won't apply */ }
.block { display: block; }
.font-semibold { font-weight: 600; }
.mb-2 { margin-bottom: 0.5rem; }
.w-full { width: 100%; }
.p-3 { padding: 0.75rem; }
.border { border-width: 1px; }
.border-gray-300 { border-color: #D1D5DB; }
.focus\\:outline-none:focus { outline: 2px solid transparent; outline-offset: 2px; }
.focus\\:border-blue-500:focus { border-color: #3B82F6; } /* Tailwind blue-500 */
.flex-wrap { flex-wrap: wrap; }
.justify-center { justify-content: center; }
.gap-4 { gap: 1rem; }
.py-3 { padding-top: 0.75rem; padding-bottom: 0.75rem; }
.min-w-\\[120px\\] { min-width: 120px; } /* Arbitrary value, Tkhtml may not support */
.bg-blue-500 { background-color: #3B82F6; }
.hover\\:bg-blue-600:hover { background-color: #2563EB; }
.bg-red-500 { background-color: var(--pup-red-500); }
.hover\\:bg-red-600:hover { background-color: var(--pup-red-600); }
.text-xl { font-size: 1.25rem; line-height: 1.75rem; }
.overflow-x-auto { overflow-x: auto; }
.min-w-full { min-width: 100%; }
.divide-y > :not([hidden]) ~ :not([hidden]) { border-top-width: 1px; border-color: #E5E7EB; }
.divide-gray-200 { border-color: #E5E7EB; }
.px-4 { padding-left: 1rem; padding-right: 1rem; }
.py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
.text-left { text-align: left; }
.text-xs { font-size: 0.75rem; line-height: 1rem; }
.font-medium { font-weight: 500; }
.uppercase { text-transform: uppercase; }
.tracking-wider { letter-spacing: 0.05em; }
.whitespace-nowrap { white-space: nowrap; }
.text-sm { font-size: 0.875rem; line-height: 1.25rem; }
.text-gray-500 { color: #6B7280; }
.text-center { text-align: center; }
.text-gray-900 { color: #111827; }
.text-gray-700 { color: #374151; }
.text-green-600 { color: #16A34A; }
.text-blue-600 { color: #2563EB; }

/* Flash Messages */
.flash-message {
    padding: 10px;
    margin-bottom: 15px;
    border-radius: 5px;
    font-weight: bold;
    text-align: center;
}
.flash-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}
.flash-error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}
"""

# --- Constants for CSS Class Names (Used to reference classes from FULL_INLINE_CSS_ADMIN) ---
PUP_BURGUNDY_CLASS = 'pup-bg-burgundy'
PUP_GOLD_CLASS = 'pup-bg-gold'
PUP_TEXT_BURGUNDY_CLASS = 'pup-text-burgundy' 

# Specific Tailwind classes used in example HTML, now defined or mapped in FULL_INLINE_CSS_ADMIN
TAILWIND_RED_800 = 'text-red-800'
PUP_DARK_BURGUNDY_HOVER_CLASS = 'hover:bg-red-900'


def create_admin_page(page_title, content_func):
    doc = dominate.document(title=f"PUP Admin - {page_title}")
    with doc.head:
        meta(charset="UTF-8")
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        style(FULL_INLINE_CSS_ADMIN) # FIX: Inline all CSS here
    
    doc.body._class = "bg-gray-50 font-sans"
    with doc.body:
        with div(_class="container mx-auto p-4 max-w-4xl"):
            # Admin Header
            with header(_class=f"{PUP_BURGUNDY_CLASS} text-white p-4 shadow-lg flex items-center justify-between mb-6"):
                with div(_class="flex items-center space-x-3"):
                    with div(_class=f"w-8 h-8 {PUP_GOLD_CLASS} rounded-full flex items-center justify-center"):
                        i(_class=f"fas fa-tools {TAILWIND_RED_800}")
                    h1(page_title, _class="text-xl font-bold")
                with nav():
                    with ul(_class="flex"):
                        li(a("Inventory", href=url_for('admin_dashboard'), _class="text-white hover:text-gray-200 mx-2"))
                        li(a("Orders (WIP)", href="#", _class="text-white hover:text-gray-200 mx-2"))

            # Flash messages
            for category, message in get_flashed_messages(with_categories=True):
                div(message, _class=f"p-3 mb-4 rounded-lg font-semibold text-sm flash-{category}")

            # Main content
            content_func()
    return doc.render()

def inventory_management_content():
    h2("Inventory Management", _class=f"text-2xl font-bold {PUP_TEXT_BURGUNDY_CLASS} mb-4")
    
    # Form for CRUD operations
    with form(action=url_for('handle_admin_action'), method="post", _class="bg-white rounded-lg shadow-lg p-6 mb-6"):
        with div(_class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4"):
            with div():
                label("Item ID (for Update/Delete):", _class="block text-gray-700 font-semibold mb-2", _for="item_id")
                input_(type="text", name="item_id", id="item_id", placeholder="e.g., 1", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500")
            with div():
                label("Item Name:", _class="block text-gray-700 font-semibold mb-2", _for="item_name")
                input_(type="text", name="item_name", id="item_name", required=True, _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500")
            with div():
                label("Quantity:", _class="block text-gray-700 font-semibold mb-2", _for="quantity")
                input_(type="number", name="quantity", id="quantity", required=True, _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500")
            with div():
                label("Price:", _class="block text-gray-700 font-semibold mb-2", _for="price")
                input_(type="text", name="price", id="price", required=True, placeholder="e.g., 150.00", _class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500")
        
        with div(_class="flex flex-wrap justify-center gap-4"):
            button("Add Item", name="action", value="add", type="submit", _class=f"flex-1 min-w-[120px] {PUP_BURGUNDY_CLASS} text-white py-3 rounded-lg font-semibold {PUP_DARK_BURGUNDY_HOVER_CLASS} transition-colors")
            button("Update Item", name="action", value="update", type="submit", _class="flex-1 min-w-[120px] bg-blue-500 text-white py-3 rounded-lg font-semibold hover:bg-blue-600 transition-colors")
            button("Delete Item", name="action", value="delete", type="submit", _class="flex-1 min-w-[120px] bg-red-500 text-white py-3 rounded-lg font-semibold hover:bg-red-600 transition-colors")
        
    h2("Current Inventory", _class=f"text-xl font-bold {PUP_TEXT_BURGUNDY_CLASS} mb-4")
    
    products = db.get_all_products()
    with div(_class="overflow-x-auto bg-white rounded-lg shadow-lg"):
        with table(_class="min-w-full divide-y divide-gray-200"):
            with thead(_class=PUP_BURGUNDY_CLASS):
                with tr():
                    th("ID", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
                    th("Name", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
                    th("Quantity (Stock)", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
                    th("Price", _class="px-4 py-2 text-left text-xs font-medium text-white uppercase tracking-wider")
            with tbody(_class="bg-white divide-y divide-gray-200"):
                if not products:
                    with tr():
                        td("No products found.", colspan="4", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500 text-center")
                for p in products:
                    with tr():
                        td(p['id'], _class="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900")
                        td(p['name'], _class="px-4 py-2 whitespace-nowrap text-sm text-gray-700")
                        td(p['stock'], _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500")
                        td(f"₱{p['price']:.2f}", _class="px-4 py-2 whitespace-nowrap text-sm text-gray-500")

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
        flash("Quantity and Price must be numbers, Item ID must be an error.", 'error')
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