import tkinter as tk
from tkinter import font
import tkinterweb
import threading
import time
from flask import Flask, send_from_directory
import os
import configparser

# CHANGE THIS LINE: from .web_pages import app as flask_app
from shop_app.web_pages import app as flask_app

# --- Configuration for Splash Screen ---
CONFIG_FILE = 'shop_app/config.ini'
def check_first_launch():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        return True
    config.read(CONFIG_FILE)
    return config.getboolean('General', 'first_launch', fallback=True)

def mark_launch_as_done():
    config = configparser.ConfigParser()
    config['General'] = {'first_launch': 'false'}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

# --- Flask Server Thread ---
def run_flask():
    # Use a different port if 5000 is taken
    flask_app.run(port=5000, debug=False)

class PupShopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PUP E-Commerce Shop")
        self.geometry("450x800")
        self.resizable(False, False)

        if check_first_launch():
            self.show_onboarding()
        else:
            self.setup_main_app()

    def show_onboarding(self):
        self.onboarding_frame = tk.Frame(self)
        self.onboarding_frame.pack(fill="both", expand=True)

        self.splash_screens = []
        splash_texts = [
            "Welcome to the PUP Shop!\n\nYour one-stop shop for Sintang Paaralan merch.",
            "Mula sa Iskolar, Para sa Iskolar\n\nSupporting student projects and initiatives.",
            "Get Started!\n\nClick below to enter the shop."
        ]
        
        for i, text in enumerate(splash_texts):
            frame = tk.Frame(self.onboarding_frame, bg="#8c1515")
            label = tk.Label(frame, text=text, font=("Helvetica", 18, "bold"), fg="white", bg="#8c1515", wraplength=300)
            label.pack(pady=100, padx=20)
            if i < len(splash_texts) - 1:
                btn = tk.Button(frame, text="Next >", command=lambda i=i: self.next_splash(i))
                btn.pack(pady=20)
            else:
                btn = tk.Button(frame, text="Get Started", command=self.finish_onboarding)
                btn.pack(pady=20)
            self.splash_screens.append(frame)
        
        self.current_splash = 0
        self.splash_screens[0].place(relx=0, rely=0, relwidth=1, relheight=1)

    def next_splash(self, current_index):
        if current_index + 1 < len(self.splash_screens):
            self.current_splash = current_index + 1
            # Simple fade transition instead of complex swipe
            self.splash_screens[current_index].place_forget()
            self.splash_screens[self.current_splash].place(relx=0, rely=0, relwidth=1, relheight=1)

    def finish_onboarding(self):
        mark_launch_as_done()
        self.onboarding_frame.destroy()
        self.setup_main_app()

    def setup_main_app(self):
        self.html_frame = tkinterweb.HtmlFrame(self, messages_enabled=False)
        self.html_frame.pack(fill="both", expand=True)

        self.create_bottom_nav()
        self.html_frame.load_url("http://127.0.0.1:5000/") # Start at login/register

    def create_bottom_nav(self):
        nav_bar = tk.Frame(self, height=60, bg="#f0f0f0", relief="raised", borderwidth=1)
        nav_bar.pack(side="bottom", fill="x")

        buttons = [("Homepage", "/home"), ("Cart", "/cart"), ("Profile", "/profile")]
        for text, url in buttons:
            btn = tk.Button(
                nav_bar, 
                text=text, 
                command=lambda u=url: self.navigate(u),
                relief="flat",
                bg="#f0f0f0"
            )
            btn.pack(side="left", fill="both", expand=True)
    
    def navigate(self, url):
        full_url = f"http://127.0.0.1:5000{url}"
        self.html_frame.load_url(full_url)


if __name__ == "__main__":
    # Start the Flask server in a daemon thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Wait a moment for the server to start
    time.sleep(1)

    # Initialize the database
    from shared.database import setup_database
    setup_database()
    
    app = PupShopApp()
    app.mainloop()