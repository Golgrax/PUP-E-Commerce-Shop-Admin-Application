import tkinter as tk
import tkinterweb
import threading
import time

# CHANGE THIS LINE: from .admin_pages import app as admin_flask_app
from admin_app.admin_pages import app as admin_flask_app

# --- Flask Server Thread for Admin ---
def run_admin_flask():
    # Use a different port to avoid conflict with the main shop app
    admin_flask_app.run(port=5001, debug=False)

class AdminApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PUP Shop - Admin Panel")
        self.geometry("800x600")

        self.html_frame = tkinterweb.HtmlFrame(self)
        self.html_frame.pack(fill="both", expand=True)
        
        # Load the admin dashboard by default
        self.html_frame.load_url("http://127.0.0.1:5001/admin")

if __name__ == "__main__":
    # Start the Admin Flask server in a daemon thread
    flask_thread = threading.Thread(target=run_admin_flask, daemon=True)
    flask_thread.start()
    
    # Wait a moment for the server to start
    time.sleep(1)
    
    # Initialize the database if not already done
    from shared.database import setup_database
    setup_database()

    app = AdminApp()
    app.mainloop()