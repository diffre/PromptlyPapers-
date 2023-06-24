from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db = mysql.connector.connect(
    host="localhost",
    user="",
    password="",
    database=""
)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Validate form data
        if not username or not email or not password:
            return "Please fill in all the required fields."

        # Insert user details into the database
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        db.commit()

        return redirect('/login')  # Redirect to the login page after successful signup

    return render_template('signup.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']

        # Validate form data and authenticate user
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

        if user:
            # Set the user ID in session or implement authentication mechanism as per your requirement
            return redirect('/dashboard')  # Redirect to the dashboard after successful login
        else:
            return "Invalid email or password."

    return render_template('login.html')

# Route for task posting
@app.route('/post_task', methods=['GET', 'POST'])
def post_task():
    if request.method == 'POST':
        # Get form data
        description = request.form['description']
        budget = request.form['budget']
        deadline = request.form['deadline']

        # Validate form data
        if not description or not budget or not deadline:
            return "Please fill in all the required fields."

        # Insert task details into the database
        cursor = db.cursor()
        cursor.execute("INSERT INTO tasks (description, budget, deadline) VALUES (%s, %s, %s)", (description, budget, deadline))
        db.commit()

        return redirect('/dashboard')  # Redirect to the dashboard after successful task posting

    return render_template('post_task.html')

# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    # Retrieve necessary data from the database (e.g., user's tasks, user's bids)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    tasks = cursor.fetchall()

    cursor.execute("SELECT * FROM bids WHERE user_id = %s", (user_id,))
    bids = cursor.fetchall()

    # Pass the retrieved data to the dashboard template for rendering
    return render_template('dashboard.html', tasks=tasks, bids=bids)

# Route for creating an order
@app.route('/create_order', methods=['POST'])
def create_order():
    # Get form data
    bid_id = request.form['bid_id']
    client_id = request.form['client_id']
    freelancer_id = request.form['freelancer_id']

    # Validate form data
    if not bid_id or not client_id or not freelancer_id:
        return "Please fill in all the required fields."

    # Retrieve necessary data from the database (e.g., selected bid)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM bids WHERE bid_id = %s", (bid_id,))
    bid = cursor.fetchone()

    if not bid:
        return "Invalid bid ID."

    # Create a new order entry in the database table for orders
    cursor.execute("INSERT INTO orders (bid_id, client_id, freelancer_id, status) VALUES (%s, %s, %s, 'pending')",
                   (bid_id, client_id, freelancer_id))
    db.commit()

    return redirect('/dashboard')  # Redirect to the dashboard after successful order creation

if __name__ == '__main__':
    app.run()