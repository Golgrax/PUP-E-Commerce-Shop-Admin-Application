import tkinter as tk
import tkinterweb
import threading
import time

from admin_app.admin_pages import app as admin_flask_app

def run_admin_flask():
    admin_flask_app.run(port=5001, debug=False)

class AdminApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PUP Shop - Admin Panel")
        self.geometry("800x600")
        self.html_frame = tkinterweb.HtmlFrame(self)
        self.html_frame.pack(fill="both", expand=True)
        self.html_frame.load_url("http://127.0.0.1:5001/admin")

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_admin_flask, daemon=True)
    flask_thread.start()
    time.sleep(1)
    from shared.database import setup_database
    setup_database()
    app = AdminApp()
    app.mainloop()
