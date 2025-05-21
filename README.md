# Grocery Store Management System 🛒

A web-based grocery store management system built with **Django** and styled using **Bootstrap 5**.  
This application supports role-based access for **customers**, **staff**, and **admin**, each with specific permissions and interfaces.

## 🔧 Features

### 👥 User Roles

- **Admin**  
  - Login via Django admin panel
- **Staff**  
  - Login
  - Add and update products (ID, name, price)
  - View and manage customer baskets (approve/deny)
  - View customer information and purchase history
- **Customers**  
  - Login
  - Add products to basket
  - View basket status and purchase history

## 🧩 Technologies Used

- **Django**
- **SQLite3** (default development DB)
- **Bootstrap 5** for responsive UI
- **Django's built-in user authentication system**

## 🗂️ Project Structure
grocery_store/

┣ grocery_store/          # Django project settings

┣ store/                  # Main app (models, views, urls, templates)

┣ templates/              # Shared templates using Bootstrap 5

┣ static/                 # Static files (CSS, JS)

┣ db.sqlite3              # Default database

┗ manage.py

## 🧪 How to Run the Project

1. **Clone the repo**  
   (If you’re setting it up from GitHub)
   ```bash
   git clone https://github.com/hokanitao/grocery-store-Django
   cd grocery-store

2.	**Create and activate virtual environment**
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate

3.	**Install dependencies**
    ```bash
    python3 -m pip install Django

4.	**Run migrations and create superuser**
    ```bash
    python3 manage.py migrate
    python3 manage.py createsuperuser

5.	**Run the development server**
    ```bash
    python3 manage.py runserver

6.	**Access the app**
  •	App: http://127.0.0.1:8000/
	•	Admin Panel: http://127.0.0.1:8000/admin/

    
