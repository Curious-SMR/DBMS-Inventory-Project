from flask import Flask, render_template, request, redirect, url_for, session, g, flash
import mysql.connector
from mysql.connector import IntegrityError
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Database Configuration - UPDATE YOUR PASSWORD HERE
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '2024A7PS0284U', # Put your recovered/new password here
    'database': 'inventory_manager'
}

def get_db():
    """Connect to the MySQL database."""
    if 'db' not in g:
        g.db = mysql.connector.connect(**DB_CONFIG)
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Close the database connection."""
    if 'db' in g:
        g.db.close()

@app.route('/')
def index():
    """Render the main page showing all products."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor(dictionary=True)
    user_id = session['user_id']
    
    # Notice we use %s for MySQL instead of ? for SQLite
    cursor.execute('SELECT * FROM product WHERE user_id = %s', (user_id,))
    products = cursor.fetchall()
    cursor.close()
    
    username = session['username']
    return render_template('index.html', products=products, username=username)

@app.route('/dashboard')
def user_dashboard():
    """Render the user dashboard with summary information."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor(dictionary=True)
    user_id = session['user_id']
    
    # Using 'AS' aliases so we can fetch by key name with dictionary=True
    cursor.execute('SELECT COUNT(*) AS count FROM product WHERE user_id = %s', (user_id,))
    total_products = cursor.fetchone()['count']
    
    cursor.execute('SELECT SUM(price * quantity) AS total FROM product WHERE user_id = %s', (user_id,))
    total_result = cursor.fetchone()['total']
    total_value = total_result if total_result else 0

    # THE ASSIGNMENT REQUIREMENT: Nested/Correlated Query
    # Finds products priced higher than their specific category average
    nested_query = """
        SELECT p1.name, p1.price, c.name AS category_name
        FROM product p1
        JOIN category c ON p1.category_id = c.id
        WHERE p1.price > (
            SELECT AVG(p2.price)
            FROM product p2
            WHERE p1.category_id = p2.category_id
        ) AND p1.user_id = %s
    """
    cursor.execute(nested_query, (user_id,))
    premium_products = cursor.fetchall()
    cursor.close()

    username = session['username']
    # You will need to update user_dashboard.html to display 'premium_products'
    return render_template('user_dashboard.html', 
                           total_products=total_products, 
                           total_value=total_value, 
                           username=username,
                           premium_products=premium_products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('INSERT INTO user (username, password) VALUES (%s, %s)', (username, hashed_password))
            db.commit()
            flash('Registration successful! Please log in.','success')
            cursor.close()
            return redirect(url_for('login'))
        except IntegrityError:
            flash('Username already exists.','error')
            cursor.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!','success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.','error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.','success')
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_product():
    """Add a new product to the database."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    name = request.form['name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    # Fallback to category 1 if you haven't added a category dropdown to your HTML form yet
    category_id = int(request.form.get('category_id', 1)) 
    user_id = session['user_id']
    
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute('SELECT * FROM product WHERE name = %s AND user_id = %s', (name, user_id))
    existing_product = cursor.fetchone()
    
    if existing_product:
        flash('Product with this name already exists.', 'error')
    else:
        if name and quantity > 0 and price > 0:
            # THE ASSIGNMENT REQUIREMENT: Calling the Stored Procedure
            cursor.callproc('AddProduct', (name, quantity, price, user_id, category_id))
            db.commit()
            flash('Product added successfully.', 'success')
        else:
            flash("Enter details properly!",'error')

    cursor.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    """Edit an existing product."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])

        cursor.execute('SELECT * FROM product WHERE name = %s AND user_id = %s AND id != %s', (name, session['user_id'], id))
        existing_product = cursor.fetchone()
        
        if existing_product:
            flash('Product with this name already exists.','error')
            cursor.close()
            return redirect(url_for('edit_product', id=id))

        cursor.execute('UPDATE product SET name = %s, quantity = %s, price = %s WHERE id = %s', (name, quantity, price, id))
        db.commit()
        flash('Product updated successfully.','success')
        cursor.close()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM product WHERE id = %s', (id,))
    product = cursor.fetchone()
    cursor.close()
    
    return render_template('manage.html', product=product, action='Edit')

@app.route('/delete/<int:id>')
def delete_product(id):
    """Delete a product from the database."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM product WHERE id = %s', (id,))
    db.commit()
    cursor.close()
    
    flash('Product deleted successfully.','success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)