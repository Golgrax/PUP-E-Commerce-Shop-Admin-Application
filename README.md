# PUP E-Commerce Shop & Admin Application

This project is a hybrid desktop application for a PUP (Polytechnic University of the Philippines) merchandise shop, built with Python. It features a Tkinter GUI that embeds a Flask web application for a modern, interactive user experience.

## Core Architecture
- **Hybrid Application**: Tkinter for the main window, navigation, and splash screens.
- **Embedded Web View**: A multi-threaded Flask server provides the UI content, which is displayed using the `tkinterweb` library.
- **Programmatic HTML**: All web pages are generated using the `dominate` Python package, not Jinja2 templates.
- **Database**: MySQL is used for all data persistence.
- **Concurrency**: The Flask server runs in a separate thread to keep the Tkinter UI responsive.
- **Two Applications**:
    1.  **Shop Application**: The main user-facing e-commerce store.
    2.  **Admin Application**: A separate, independent app for inventory and order management.

## Project Structure

```
PUP_Shop_App/
├── shop_app/
│   ├── main.py
│   └── web_pages.py
├── admin_app/
│   ├── admin_main.py
│   └── admin_pages.py
├── shared/
│   └── database.py
├── assets/
│   ├── images/
│   │   ├── pup_logo.png
│   │   ├── product_lanyard_1.png
│   │   ├── product_lanyard_2.png
│   │   ├── product_jeepney.png
│   │   ├── product_tote_1.png
│   │   ├── product_tote_2.png
│   │   └── product_shirt.png
│   ├── fonts/
│   │   └── RocaOne-Bold.ttf
│   └── css/
│       └── style.css
└── requirements.txt
```

## Setup and Installation

**1. Prerequisites:**
- Python 3.8+
- MySQL Server installed and running.

**2. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**3. Database Setup:**
- Open the `shared/database.py` file.
- **Crucially, update the `DB_CONFIG` dictionary** with your MySQL username, password, and host.
```python
DB_CONFIG = {
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'host': '127.0.0.1',
    'database': 'pup_shop_db' # This DB will be created automatically
}
```
- The script will automatically create the `pup_shop_db` database and all necessary tables with placeholder data when you run either application for the first time.

**4. Assets:**
- Place all required images in the `assets/images/` directory.
- Place the `RocaOne-Bold.ttf` font file in the `assets/fonts/` directory.

**5. Running the Applications:**

- **To run the main Shop Application:**
  ```bash
  python shop_app/main.py
  ```
- **To run the separate Admin Application:**
  ```bash
  python admin_app/admin_main.py
  ```

## How It Works

- When `main.py` or `admin_main.py` is executed, it starts a Tkinter main loop.
- It also starts a Flask web server in a separate daemon thread.
- The Tkinter window contains a `tkinterweb.HtmlFrame` widget.
- UI interactions (like clicking bottom navigation buttons) command the `HtmlFrame` to load URLs from the local Flask server (e.g., `http://127.0.0.1:5000/home`).
- The Flask routes, defined in `web_pages.py` and `admin_pages.py`, use the `dominate` library to build HTML responses on the fly, fetching data from the MySQL database as needed.

## Onboarding Screens
The main shop application features a set-of three onboarding splash screens that appear **only on the very first launch**. A `config.ini` file is created to track this. To see the splash screens again, simply delete `shop_app/config.ini`.