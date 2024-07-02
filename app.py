from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify,json
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import TransactionNotFound
from eth_account import Account
import logging
import smtplib
from email.mime.text import MIMEText
from functools import wraps
from email.mime.multipart import MIMEMultipart
from web3.exceptions import TransactionNotFound

app = Flask(__name__)
app.static_folder = 'static'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '5544'
app.config['MYSQL_DB'] = 'medical_store'
mysql = MySQL(app)

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))


# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load contract JSON file
contract_file = 'build/contracts/MedicalSupplyChain.json'  # Replace 'YourContract' with your contract name
with open(contract_file) as f:
    contract_data = json.load(f)

# Extract contract ABI and address
contract_abi = contract_data['abi']
contract_address = "0x1FEF4b74ce59FFA4fB4BAF2da5Aa1A26fCD0F19E"

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Set up private key
private_key = '0x7b135724cb8efca83849803beae2969d111a5da31b408b54acb74d91abff8949' 

# Create an account object from the private key
account = Account.from_key(private_key)

# Get the sender's Ethereum address
sender_address = account.address

# Set the default account to use for transactions
web3.eth.default_account = sender_address

# Define a decorator to restrict access based on user role
def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if the user is logged in
            if 'loggedin' not in session:
                flash('You need to log in first.', 'error')
                return redirect(url_for('login'))
            # Check if the user has any of the required roles
            user_role = session.get('role')
            print("User Role:", user_role)  # Debugging message
            print("Required Roles:", roles)  # Debugging message
            if user_role not in roles:
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('dashboard'))  # Redirect to a suitable page
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/')
def index():
    # Check if connected to Ganache by attempting to get the block number
    try:
        block_number = web3.eth.block_number
        print("Connected to Ganache!")
        return render_template('login.html')
    except Exception as e:
        print(f"Failed to connect to Ganache: {e}") 
        return render_template('login.html')

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password,))
        user = cursor.fetchone()
        
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            session['role'] = user['role']  # Set the user's role in the session
            message = 'Logged in successfully!'
            def get_medicines_in_stock_count():
                """
                Get the count of medicines that are in stock.
                """
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT COUNT(*) FROM medicine WHERE available_qty > 0")
                    in_stock_count = cur.fetchone()[0]
                return in_stock_count


            def get_medicines_out_of_stock_count():
                """
                Get the count of medicines that are out of stock.
                """
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT COUNT(*) FROM medicine WHERE available_qty <= 0")
                    out_of_stock_count = cur.fetchone()[0]
                return out_of_stock_count


            def get_total_purchases():
                """
                Get the total number of purchases made.
                """
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT COUNT(*) FROM purchases")
                    total_purchases = cur.fetchone()[0]
                return total_purchases


            def get_total_sales():
                """
                Get the total number of sales made.
                """
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT SUM(total_amount) FROM bill")
                    total_sales = cur.fetchone()[0]
                return total_sales

            medicines_in_stock = get_medicines_in_stock_count()
            medicines_out_of_stock = get_medicines_out_of_stock_count()
            total_purchases = get_total_purchases()
            total_sales = get_total_sales()
            
            connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM medicine WHERE available_qty<5')
            medicines = [{'medicine_id': row[0], 'medicine_name': row[1],'category_name':row[3],'company':row[4],'single_pack_quantity':row[5],'location_rack':row[7],'added_on':row[8],'updated_on':row[9], 'available_qty':row[6]} for row in cursor.fetchall()]
            cursor.close()
            connection.close()
        
            return render_template('dashboard.html', medicines=medicines, message=message, medicines_in_stock=medicines_in_stock, medicines_out_of_stock=medicines_out_of_stock, total_purchases=total_purchases, total_sales=total_sales )
        else:
            message = 'Please enter correct email/password!'
    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'role' in request.form:
        userName = request.form['name'] 
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            flash('Account already exists!',category='error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not userName or not password or not role or not email:
            message = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO user_request (name, email, password, role) VALUES (%s, %s, %s, %s)', (userName, email, password, role,))
            mysql.connection.commit()
            message = 'You have successfully sent register request, once you are accepted you will receive a mail!'
    elif request.method == 'POST': 
        message = 'Please fill out the form!'
    return render_template('register.html', message=message)


@app.route('/dashboard')
def dashboard():
    connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM medicine WHERE available_qty<5')
    medicines = [{'medicine_id': row[0], 'medicine_name': row[1],'category_name':row[3],'company':row[4],'single_pack_quantity':row[5],'location_rack':row[7],'added_on':row[8],'updated_on':row[9], 'available_qty':row[6]} for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    if 'loggedin' in session:
        medicines_in_stock = get_medicines_in_stock_count()
        medicines_out_of_stock = get_medicines_out_of_stock_count()
        total_purchases = get_total_purchases()
        total_sales = get_total_sales()

        return render_template('dashboard.html', medicines=medicines, medicines_in_stock=medicines_in_stock, medicines_out_of_stock=medicines_out_of_stock, total_purchases=total_purchases, total_sales=total_sales)
    return redirect(url_for('dashboard'))
def get_medicines_in_stock_count():
    """
    Get the count of medicines that are in stock.
    """
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM medicine WHERE available_qty > 0")
        in_stock_count = cur.fetchone()[0]
    return in_stock_count


def get_medicines_out_of_stock_count():
    """
    Get the count of medicines that are out of stock.
    """
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM medicine WHERE available_qty <= 0")
        out_of_stock_count = cur.fetchone()[0]
    return out_of_stock_count


def get_total_purchases():
    """
    Get the total number of purchases made.
    """
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM purchases")
        total_purchases = cur.fetchone()[0]
    return total_purchases


def get_total_sales():
    """
    Get the total number of sales made.
    """
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT SUM(total_amount) FROM bill")
        total_sales = cur.fetchone()[0]
    return total_sales
    

@app.route('/user_management')
@role_required(['admin'])
def user_management():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user')
    user = [{'userid': row[0], 'name': row[1],'email':row[2],'password':row[3],'role':row[4],'added_on':row[5],'updated_on':row[6]} for row in cur.fetchall()]

    return render_template('user_management.html', user=user)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        passwords = request.form['password']
        role = request.form['role']
        
        # Check if any field is empty
        if not name or not email or not passwords or not role:
            error_message = 'All fields are required'
            return render_template('add_user.html', error=error_message)

        # Perform the insertion into the database
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO user (name, email, password, role) VALUES (%s, %s, %s, %s)',
            (name, email, passwords, role)
        )
        mysql.connection.commit()
        cur.close()

        # Send acceptance email
        sender_email = 'rahulgummula9@gmail.com'  # Your email address
        receiver_email = email  # Receiver's email address
        password = 'jill eneb ascj qftk'  # Your email password
        
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = 'Medical Store Registration Accepted'

        body = f'Hello {name},\n\nYour are registered in Medical Store. You can now login with the provided credentials.\n\nUsername: {email}\nPassword: {passwords}\nRole: {role}\n\nThank you!'
        message.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            flash('Registration accepted. Email sent to the user.', 'success')
            print("Mail sent")
        except Exception as e:
            flash('An error occurred while sending the email.', 'error')
            print(f'Error: {e}')

        return redirect(url_for('user_management'))

    return render_template('add_user.html')



@app.route('/user_requests')
def user_requests():
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user_request')
    user_requests = [{'userid': row[0], 'name': row[1],'email':row[2],'password':row[3],'role':row[4]} for row in cur.fetchall()]
    print(user_requests)
    mysql.connection.commit()
    cur.close()

    return render_template('user_requests.html', user_requests=user_requests)


@app.route('/reject_user/<int:userid>', methods=['GET'])
def reject_user(userid):
    connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')

    cursor = connection.cursor()

    cursor.execute('DELETE FROM user_request WHERE userid = %s', (userid,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('user_requests'))


@app.route('/accept_user/<int:userid>', methods=['GET', 'POST'])
def accept_user(userid):
    connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')

    # Fetch the user details from the user_request table
    cur = connection.cursor()
    cur.execute('SELECT * FROM user_request WHERE userid = %s', (userid,))
    user_request = cur.fetchone()
    cur.close()

    if user_request:
        # Extract user details
        name = user_request[1]
        email = user_request[2]
        passwords = user_request[3]
        role = user_request[4]
        
        # Send acceptance email
        sender_email = 'rahulgummula9@gmail.com'  # Your email address
        receiver_email = email  # Receiver's email address
        password = 'jill eneb ascj qftk'  # Your email password
        
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = 'Registration Accepted'

        body = f'Hello {name},\n\nYour registration request has been accepted. You can now login with the provided credentials.\n\nUsername: {email}\nPassword: {passwords}\nRole: {role}\n\nThank you!'
        message.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            flash('Registration accepted. Email sent to the user.', 'success')
        except Exception as e:
            flash('An error occurred while sending the email.', 'error')
            print(f'Error: {e}')

        # Insert the user details into the user table
        cur = connection.cursor()
        cur.execute('INSERT INTO user (name, email, password, role) VALUES (%s, %s, %s, %s)', (name, email, passwords, role,))
        connection.commit()
        cur.close()

        # Delete the user request from the user_request table
        cur = connection.cursor()
        cur.execute('DELETE FROM user_request WHERE userid = %s', (userid,))
        connection.commit()
        cur.close()

    connection.close()

    return redirect(url_for('user_requests'))

@app.route('/edit_user/<int:userid>', methods=['GET', 'POST'])
def edit_user(userid):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        passwords = request.form['password']
        role = request.form['role']
        
        # Check if any field is empty
        if not name or not email or not passwords or not role:
            error_message = 'All fields are required'
            return render_template('edit_user.html', error=error_message)

        # Perform the update in the database
        cur = mysql.connection.cursor()
        cur.execute(
            'UPDATE user SET name=%s, email=%s, password=%s, role=%s WHERE userid=%s',
            (name, email, passwords, role, userid)
        )
        mysql.connection.commit()
        cur.close()

        flash('User details updated successfully', 'success')
        return redirect(url_for('user_management'))
    
    # Fetch user details from the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user WHERE userid = %s', (userid,))
    user = cur.fetchone()
    cur.close()

    if user:
        user_details = {
            'userid': user[0],
            'name': user[1],
            'email': user[2],
            'password': user[3],
            'role': user[4]
        }
        return render_template('edit_user.html', user=user_details)
    else:
        flash('User not found', 'error')
        return redirect(url_for('user_management'))

@app.route('/delete_user/<int:userid>', methods=['GET'])
def delete_user(userid):
    connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')

    cursor = connection.cursor()
    cursor.execute('SELECT role from user')
    role=cursor.fetchall()
    connection.commit()
    cursor.close()
    
    if role=="admin":
        cursor = connection.cursor()
        cursor.execute('DELETE FROM user WHERE userid = %s', (userid,))
        connection.commit()
        cursor.close()
        connection.close()
    

    return redirect(url_for('user_management'))


@app.route('/manage_medicines')
@role_required(['admin'])
def manage_medicines():
    cur = mysql.connection.cursor()
    
    cur.execute('SELECt * FROM medicine')
    medicines = [{'medicine_id': row[0], 'medicine_name': row[1],'category_name':row[3],'company':row[4],'single_pack_quantity':row[5],'location_rack':row[7],'added_on':row[8],'updated_on':row[9], 'available_qty':row[6]} for row in cur.fetchall()]

    return render_template('manage_medicines.html', medicines=medicines)

@app.route('/add_medicine', methods=['GET', 'POST'])
def add_medicine():
    if request.method == 'POST':
        # Process form submission
        medicine_name = request.form['medicine_name']
        company = request.form['company']
        pack_detail = request.form['pack_detail']
        category = request.form['category']
        location_rack = request.form['location_rack']
        
        # Check if medicine name is provided
        if not medicine_name:
            error_message = 'Medicine Name cannot be empty'
            return render_template('add_medicine.html', error=error_message)

        # Perform the insertion into the database
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO medicine (medicine_name, company, single_pack_quantity, category_name, location_rack) VALUES (%s, %s, %s, %s, %s)',
            (medicine_name, company, pack_detail, category, location_rack)
        )
        mysql.connection.commit()
        cur.close()

        # Redirect to the page displaying all medicines
        return redirect(url_for('manage_medicines'))
    
    # If the request method is GET, fetch categories from the database and render the form
    cur = mysql.connection.cursor()
    cur.execute("SELECT category_name FROM categories")
    categories = cur.fetchall()
    cur.close()
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT company_name FROM companies")
    companies = cur.fetchall()
    cur.close()
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT rack_name FROM location_rack")
    racks = cur.fetchall()
    cur.close()

    return render_template('add_medicine.html', categories=categories, companies=companies, racks=racks)

@app.route('/edit_medicines/<int:medicine_id>', methods=['GET', 'POST'])
def edit_medicines(medicine_id):
    if 'loggedin' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM medicine WHERE medicine_id = %s', (medicine_id,))
        medicine = cursor.fetchone()

        if not medicine:
            flash('Medicine not found', 'error')
            return redirect(url_for('manage_medicines'))

        if request.method == 'POST':
            medicine_name = request.form['medicine_name']
            company = request.form['company']
            pack_detail = request.form['pack_detail']
            available_qty = request.form['available_qty']
            category = request.form['category']
            location_rack = request.form['location_rack']

            sql_query = '''
                UPDATE medicine 
                SET medicine_name = %s, company = %s, available_qty = %s,
                single_pack_quantity = %s, category_name = %s, location_rack = %s 
                WHERE medicine_id = %s
            '''
            values = (medicine_name, company, available_qty, pack_detail, category, location_rack, medicine_id)
            cursor.execute(sql_query, values)
            mysql.connection.commit()

            flash('Medicine updated successfully', 'success')
            return redirect(url_for('manage_medicines'))

    except Exception as e:
        print(f"Error updating medicine: {str(e)}")
        flash('An error occurred while updating the medicine', 'error')
        
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM medicine WHERE medicine_id = %s', (medicine_id,))
    medicine = cursor.fetchone()
    cursor.close()
    medicine_details={
        'medicine_id' : medicine[0],
        'medicine_name' : medicine[1],
        'category_name' : medicine[3],
        'company' : medicine[4],
        'single_pack_quantity' : medicine[5],
        'available_qty' : medicine[6],
        'location_rack' : medicine[7],
        'added_on' : medicine[8],
        'updated_on' : medicine[9]
    }
    cur = mysql.connection.cursor()
    cur.execute("SELECT category_name FROM categories")
    categories = cur.fetchall()
    cur.close()
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT company_name FROM companies")
    companies = cur.fetchall()
    cur.close()
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT rack_name FROM location_rack")
    racks = cur.fetchall()
    cur.close()
    
    return render_template('edit_medicines.html', medicine=medicine_details, categories=categories, companies=companies, racks=racks)


@app.route('/delete_medicine/<int:medicine_id>', methods=['GET'])
def delete_medicine(medicine_id):
    connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')

    cursor = connection.cursor()

    cursor.execute('DELETE FROM medicine WHERE medicine_id = %s', (medicine_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('manage_medicines'))

@app.route('/display_categories')
@role_required(['admin'])
def display_categories():
    connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return render_template('display_categories.html', categories=categories)

# Route for adding a category (similar to the previous example)
@app.route('/add_category_display', methods=['GET', 'POST'])
def add_category_display():
    if request.method == 'POST':
        category_name = request.form['category_name']

        # Check if category_name is not empty before inserting into the database
        if not category_name:
            error_message = 'Category Name cannot be empty'
            return render_template('add_category_display.html', error=error_message)

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO categories (category_name) VALUES (%s)', (category_name,))
        mysql.connection.commit()

        # Optionally, you can redirect to the display_categories page after successfully adding a category
        return redirect(url_for('display_categories'))

    # If the request method is GET, simply render the add_category_display.html template
    return render_template('add_category_display.html')

@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category_display(category_id):
    
    connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')
    
    if request.method == 'POST':
        category_name = request.form['category_name']

        # Check if category_name is not empty before inserting into the database
        if not category_name:
            error_message = 'Category Name cannot be empty'
            return render_template('add_category_display.html', error=error_message)

        cur = mysql.connection.cursor()
        cur.execute('UPDATE categories SET category_name=%s where category_id=%s', (category_name, category_id))
        mysql.connection.commit()

        # Optionally, you can redirect to the display_categories page after successfully adding a category
        return redirect(url_for('display_categories'))

    
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM categories WHERE category_id = %s', (category_id,))
    category = cursor.fetchone()

    category_data = {
        'category_id': category[0], 
        'category_name': category[1],
        'added_on' : category[2],
        'updated_on' : category[3]
        }

    # If the request method is GET, simply render the add_category_display.html template
    return render_template('edit_category_display.html', category=category_data)

@app.route('/remove_category_display/<int:category_id>', methods=['GET'])
def remove_category_display(category_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM categories WHERE category_id = %s', (category_id,))
    mysql.connection.commit()

    flash('Category deleted successfully', 'success')
    return redirect(url_for('display_categories'))


@app.route('/location_rack')
@role_required(['admin'])
def location_rack():
    connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM location_rack')
    location_rack = [dict(rack_id=row[0], rack_name=row[1], added_on=row[2], updated_on=row[3]) for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return render_template('location_rack.html', location_rack=location_rack)

@app.route('/add_location_rack', methods=['GET', 'POST'])
def add_location_rack():
    if request.method == 'POST':
        rack_name = request.form['rack_name']

        if not rack_name:
            error_message = 'Rack Name cannot be empty'
            return render_template('add_location_rack.html', error=error_message)

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO location_rack (rack_name) VALUES (%s)', (rack_name,))
        mysql.connection.commit()

        return redirect(url_for('location_rack'))

    return render_template( 'add_location_rack.html' )

@app.route('/edit_location_rack/<rack_id>', methods=['GET', 'POST'])
def edit_location_rack(rack_id):
    if request.method == 'POST':
        rack_name = request.form['rack_name']

        if not rack_name:
            error_message = 'Rack Name cannot be empty'
            return render_template('edit_location_rack.html', error=error_message, rack=rack)

        connection = mysql.connection
        cur = connection.cursor()
        cur.execute('UPDATE location_rack SET rack_name = %s WHERE rack_id = %s', (rack_name, rack_id))
        connection.commit()
        cur.close()

        return redirect(url_for('location_rack'))
    
    connection = mysql.connection
    cur = connection.cursor()
    cur.execute('SELECT * FROM location_rack WHERE rack_id = %s', (rack_id,))
    rack = cur.fetchone()
    cur.close()

    rack_details = {
        'rack_id': rack[0],
        'rack_name': rack[1],
        'added_on': rack[2],
        'updated_on': rack[3]
    }

    return render_template('edit_location_rack.html', rack=rack_details)


@app.route('/remove_location_rack/<int:rack_id>', methods=['GET'])
def remove_location_rack(rack_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM location_rack WHERE rack_id = %s', (rack_id,))
    mysql.connection.commit()

    flash('Rack deleted successfully', 'success')
    return redirect(url_for('location_rack'))


@app.route('/medicine_company')
@role_required(['admin'])
def medicine_company():
    connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM companies')
    companies = [dict(company_id=row[0],company_name=row[1], company_short_name=row[2], added_on=row[3],updated_on=row[4]) for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return render_template('medicine_company.html', companies=companies)

@app.route('/add_company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        company_name = request.form['company_name']
        company_short_name = request.form['company_short_name']

        if not company_name or not company_short_name:
            error_message = 'Rack Name cannot be empty'
            return render_template('add_company.html', error=error_message)

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO companies (company_name, company_short_name) VALUES (%s, %s)', (company_name, company_short_name))
        mysql.connection.commit()

        return redirect(url_for('medicine_company'))

    return render_template('add_company.html')

@app.route('/edit_company/<int:company_id>', methods=['GET', 'POST'])
def edit_company(company_id):
    if request.method == 'POST':
        company_name = request.form['company_name']
        company_short_name = request.form['company_short_name']
        
        if not company_name or not company_short_name:
            error_message = 'Company name and company short name cannot be empty'
            return render_template('edit_company.html', error=error_message)

        # Update the company details in the database
        connection = mysql.connection
        cur = connection.cursor()
        cur.execute('UPDATE companies SET company_name = %s, company_short_name = %s WHERE company_id = %s', (company_name, company_short_name, company_id))
        connection.commit()
        cur.close()

        return redirect(url_for('medicine_company'))

    connection = mysql.connection
    cur = connection.cursor()
    cur.execute('SELECT * FROM companies WHERE company_id = %s', (company_id,))
    company = cur.fetchone()
    cur.close()
    
    company_details={
        'company_id': company[0],
        'company_name': company[1],
        'company_short_name': company[2],
        'added_on': company[3],
        'updated_on': company[4]
    }
    return render_template('edit_company.html', company=company_details)


@app.route('/delete_company/<int:company_id>', methods=['GET'])
def delete_company(company_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM companies WHERE company_id = %s', (company_id,))
    mysql.connection.commit()

    flash('Company deleted successfully', 'success')
    return redirect(url_for('medicine_company'))

@app.route('/medicine_purchase')
@role_required(['admin'])
def medicine_purchase():
    connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM purchases')
    purchases = [dict(purchase_id=row[0],medicine_name=row[1], batch_no=row[2], supplier_name=row[3], quantity=row[4], available_qty=row[5], price_per_unit=row[6], total_cost=row[7], mfg_date=row[8],expiry_date=row[9],sale_price=row[10], purchase_date=row[11]) for row in cursor.fetchall()]
    cursor.close()
    connection.close()

    return render_template('medicine_purchase.html', purchases=purchases)

@app.route('/add_purchase', methods=['GET', 'POST'])
@role_required(['admin'])
def add_purchase():
    if request.method == 'POST':
        medicine_name = request.form['medicine_name']
        supplier_name = request.form['supplier_name']
        quantity = request.form['quantity']
        price_per_unit = request.form['price_per_unit']
        mfg_date = request.form['mfg_date']
        expiry_date = request.form['expiry_date']
        batch_no = request.form['batch_no']
        sale_price = request.form['sale_price']

        # Check if all fields are filled
        if not medicine_name or not supplier_name or not quantity or not price_per_unit or not mfg_date or not expiry_date or not batch_no or not sale_price:
            error_message = 'All fields must be filled'
            return render_template('add_purchase.html', error=error_message)

        # Calculate available quantity
        connection = mysql.connection
        with connection.cursor() as cur:
            cur.execute("SELECT SUM(quantity) FROM purchases WHERE medicine_name = %s", (medicine_name,))
            total_quantity_purchased = cur.fetchone()[0]
            if total_quantity_purchased is None:
                total_quantity_purchased = 0
            available_qty = int(total_quantity_purchased) + int(quantity)

        # Calculate total cost
        total_cost = int(quantity) * float(price_per_unit)
        total_cost_in_ether = float(total_cost * 0.0000033)
        # Insert into purchases table
        with connection.cursor() as cur:
            cur.execute('INSERT INTO purchases (medicine_name, supplier_name, quantity, available_qty, price_per_unit, total_cost, mfg_date, expiry_date, batch_no, sale_price, total_cost_in_ether) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (medicine_name, supplier_name, quantity, available_qty, price_per_unit, total_cost, mfg_date, expiry_date, batch_no, sale_price, total_cost_in_ether))

            cur.execute('UPDATE medicine SET available_qty = %s WHERE medicine_name = %s', (available_qty, medicine_name))
            
            connection.commit()
        
        connection = mysql.connection
        with connection.cursor() as cur:
            cur.execute("SELECT medicine_id FROM medicine WHERE medicine_name = %s", (medicine_name,))
            medicine_id = cur.fetchone()[0]
        

        return render_template('payment.html', medicine_id=medicine_id,medicine_name=medicine_name, supplier_name=supplier_name, quantity=quantity, price_per_unit=price_per_unit, total_cost=total_cost, total_cost_in_ether=total_cost_in_ether)

    # Fetch medicine and supplier names for rendering the form
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT medicine_name FROM medicine")
        medicines = cur.fetchall()
        cur.execute("SELECT supplier_name FROM supplier")
        suppliers = cur.fetchall()

    return render_template('add_purchase.html', suppliers=suppliers, medicines=medicines)

@app.route('/payment/<int:medicine_id>/<string:supplier_name>/<string:medicine_name>/<int:quantity>/<float:price_per_unit>/<float:total_cost>/<float:total_cost_in_ether>', methods=['POST'])
def payment(medicine_id, supplier_name, medicine_name, quantity, price_per_unit, total_cost, total_cost_in_ether):
    if request.method == 'POST':
        # Retrieve form data
        amount = float(request.form['amount'])
        recipient_address = request.form['recipient_address']
        
        if amount != total_cost_in_ether:
            message="Amount must be equal to Total Cost In Ether"
            flash(message)
            
            return render_template('payment.html', p_id=p_id, message=message, medicine_id=medicine_id, supplier_name=supplier_name,medicine_name=medicine_name, quantity=quantity, price_per_unit=price_per_unit, total_cost=total_cost, total_cost_in_ether=total_cost_in_ether)

        
        # Convert amount to wei (1 Ether = 10^18 Wei)
        amount_wei = int(amount * 10**18)

        # Get the currently connected account (assume it's unlocked)
        account = web3.eth.accounts[0]  # Update with your account index
        
        gas_price_gwei = 50
        gas_price_wei = gas_price_gwei * 10**9
        
        # Prepare transaction data
        tx_data = {
            'from': account,
            'value': amount_wei,
            'gas': 2000000,  # Adjust gas limit as needed
            'gasPrice': gas_price_wei,  # Adjust gas price as needed
        }

        tx_hash = contract.functions.purchaseMedicine(medicine_id, quantity).transact(tx_data)

        try:
            # Wait for transaction receipt
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        except TransactionNotFound:
            return "Transaction not found."

        total_cost_in_ether = float(total_cost * 0.0000033)
        
        return render_template('payment_confirmation.html', medicine_id=medicine_id, supplier_name=supplier_name, medicine_name=medicine_name, price_per_unit=price_per_unit, quantity=quantity, total_cost=total_cost, total_cost_in_ether=total_cost_in_ether)

    total_cost_in_ether = float(total_cost * 0.0000033)
    return render_template('payment.html', medicine_id=medicine_id, supplier_name=supplier_name,medicine_name=medicine_name, quantity=quantity, price_per_unit=price_per_unit, total_cost=total_cost)

@app.route('/payment_confirmation/<int:medicine_id>/<string:medicine_name>/<string:supplier_name>/<int:quantity>/<float:price_per_unit>/<float:total_cost>/<float:total_cost_in_ether>')
def payment_confirmation(p_id,medicine_id,medicine_name,supplier_name, quantity, price_per_unit, total_cost,total_cost_in_ether):
    
    return render_template('payment_confirmation.html', medicine_id=medicine_id,supplier_name=supplier_name,medicine_name=medicine_name, quantity=quantity, price_per_unit=price_per_unit, total_cost=total_cost, total_cost_in_ether=total_cost_in_ether)


@app.route('/receipt/<int:purchase_id>')
def receipt(purchase_id):
    connection = mysql.connection
    with connection.cursor() as cur:
            cur.execute('SELECT * FROM purchases WHERE purchase_id = %s', (purchase_id,))
            receipts=[dict(purchase_id=row[1],medicine_name=row[1], supplier_name=row[3], price_per_unit=row[6], quantity=row[4], total_cost=row[7], total_cost_in_ether=row[12])for row in cur.fetchall()]
            connection.commit()
    return render_template('receipt.html',  receipts=receipts)


@app.route('/edit_purchase/<int:purchase_id>', methods=['GET','POST'])
def edit_purchase():
    if request.method == 'POST':
        medicine_name = request.form['medicine_name']
        supplier_name = request.form['supplier_name']
        quantity = request.form['quantity']
        price_per_unit = request.form['price_per_unit']
        mfg_date = request.form['mfg_date']
        expiry_date = request.form['expiry_date']
        batch_no = request.form['batch_no']
        sale_price = request.form['sale_price']

        if not medicine_name or not supplier_name or not quantity or not price_per_unit or not mfg_date or not expiry_date or not batch_no or not sale_price:
            error_message = 'All fields must be filled'
            return render_template('add_purchase.html', error=error_message)

        available_qty=0
        total_cost =  int(quantity)*float(price_per_unit)
        
        connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')
        cur = connection.cursor()
        cur.execute('UPDATE purchases SET (medicine_name , supplier_name ,quantity, available_qty ,price_per_unit, total_cost ,mfg_date ,expiry_date , batch_no ,sale_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (medicine_name , supplier_name ,quantity, available_qty ,price_per_unit, total_cost ,mfg_date ,expiry_date , batch_no ,sale_price))
        connection.commit()
        cur.close()
        connection.close()

        return redirect(url_for('medicine_purchase'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT medicine_name FROM medicine")
    medicines = cur.fetchall()
    cur.close()
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT supplier_name FROM supplier")
    suppliers = cur.fetchall()
    cur.close()
    return render_template('edit_purchase.html', suppliers=suppliers, medicines=medicines)


@app.route('/delete_purchase/<int:purchase_id>', methods=['GET'])
def delete_purchase(purchase_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM purchases WHERE purchase_id = %s', (purchase_id,))
    mysql.connection.commit()

    flash('Supplier deleted successfully', 'success')
    return redirect(url_for('medicine_purchase'))

@app.route('/medicine_supplier')
@role_required(['admin'])
def medicine_supplier():
    connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM supplier')
    supplier = [dict(supplier_id=row[0], supplier_name=row[1], address=row[2], contact_no=row[3], email_id=row[4], added_on=row[5], updated_on=row[6]) for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return render_template('medicine_supplier.html', supplier=supplier)

@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        supplier_name = request.form['supplier_name']
        address = request.form['address']
        contact_no = request.form['contact_no']
        email_id = request.form['email_id']

        if not supplier_name or not address or not email_id or not contact_no:
            error_message = 'All fields must be filled'
            return render_template('add_supplier.html', error=error_message)

        connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')
        cur = connection.cursor()
        cur.execute('INSERT INTO supplier (supplier_name, address, contact_no, email_id) VALUES (%s, %s, %s, %s)', (supplier_name, address, contact_no, email_id))
        connection.commit()
        cur.close()
        connection.close()

        return redirect(url_for('medicine_supplier'))

    return render_template('add_supplier.html')

@app.route('/edit_supplier/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    if request.method == 'POST':
        supplier_name = request.form['supplier_name']
        address = request.form['address']
        contact_no = request.form['contact_no']
        email_id = request.form['email_id']

        if not supplier_name:
            error_message = 'Supplier Name cannot be empty'
            return render_template('edit_supplier.html', error=error_message)

        cur = mysql.connection.cursor()
        cur.execute('UPDATE supplier SET supplier_name = %s, address = %s, contact_no = %s, email_id = %s WHERE supplier_id = %s', (supplier_name, address, contact_no, email_id, supplier_id))
        mysql.connection.commit()
        cur.close()

        flash('Supplier updated successfully', 'success')
        return redirect(url_for('medicine_supplier'))

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM supplier WHERE supplier_id = %s', (supplier_id,))
    supplier = cur.fetchone()
    cur.close()

    if supplier:
        supplier_details = {
            'supplier_id': supplier[0],
            'supplier_name': supplier[1],
            'contact_no': supplier[2],
            'email_id': supplier[3],
            'address': supplier[4],
            'added_on': supplier[5],
            'updated_on': supplier[6]
        }
    else:
        flash('Supplier not found', 'error')
        return redirect(url_for('supplier_management'))

    return render_template('edit_supplier.html', supplier=supplier_details)

@app.route('/delete_supplier/<int:supplier_id>', methods=['GET'])
def delete_supplier(supplier_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM supplier WHERE supplier_id = %s', (supplier_id,))
    mysql.connection.commit()

    flash('Supplier deleted successfully', 'success')
    return redirect(url_for('medicine_supplier'))


@app.route('/billing')
def billing():
    connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM bill')
    billing = [dict(bill_id=row[0], customer_name=row[1], doctor_name=row[2], total_amount=row[3], added_on=row[4], updated_on=row[5]) for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return render_template('billing.html', billing=billing)

@app.route('/add_bill', methods=['GET', 'POST'])
def add_bill():
    if request.method == "POST":
        customer_name = request.form['customer_name']
        doctor_name = request.form['doctor_name']
        medicine_name = request.form['medicine_name']
        
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT sale_price FROM purchases WHERE medicine_name = %s ORDER BY purchase_date DESC LIMIT 1", (medicine_name,))
        mrp_data = cur.fetchone()
        cur.execute("SELECT batch_no FROM purchases WHERE medicine_name = %s", (medicine_name,))
        batch_no = cur.fetchone()
        cur.execute("SELECT * FROM medicine WHERE medicine_name = %s", (medicine_name,))
        selected_medicine = cur.fetchone()
        
        if selected_medicine:
            medicine_id = selected_medicine[0]
            category_name = selected_medicine[3]
            company_name = selected_medicine[4]
            
            # Insert the selected medicine into the cart table
            cur.execute('INSERT INTO cart (customer_name, medicine_id, medicine_name, doctor_name, category_name, company_name, batch_no, mrp_data) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                        (customer_name,medicine_id, medicine_name, doctor_name, category_name, company_name, batch_no, mrp_data))
            mysql.connection.commit()
        else:
            flash("Medicine not found", "error")

        cur.close()
        
    # Fetch the cart contents from the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cart')
    cart_val = [dict(cart_id=row[0], customer_name=row[1], medicine_id=row[3], medicine_name=row[4], doctor_name=row[2], category_name=row[5], company_name=row[6], batch_no=row[7], mrp_data=row[8]) for row in cur.fetchall()]
    cur.close()
    
    # Fetch all medicines for the dropdown menu
    cur = mysql.connection.cursor()
    cur.execute("SELECT medicine_name FROM medicine")
    medicines = cur.fetchall()
    cur.close()
    
    return render_template('add_bill.html', medicines=medicines, cart_val=cart_val)

@app.route('/delete_bill/<int:bill_id>', methods=['GET'])
def delete_bill(bill_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM bill WHERE bill_id = %s', (bill_id,))
    mysql.connection.commit()

    flash('Cart item deleted successfully', 'success')
    return redirect(url_for('billing'))

@app.route('/delete_cart_item/<int:cart_id>', methods=['GET'])
def delete_cart_item(cart_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM cart WHERE cart_id = %s', (cart_id,))
    mysql.connection.commit()

    flash('Cart item deleted successfully', category='success')
    return redirect(url_for('add_bill'))

@app.route('/empty_cart', methods=['GET'])
def empty_cart():
    cur = mysql.connection.cursor()
    cur.execute('TRUNCATE TABLE cart')  # Corrected syntax
    mysql.connection.commit()

    flash('Emptied cart successfully', 'success')
    return redirect(url_for('add_bill'))

@app.route('/process_cart', methods=['POST'])
def process_cart():
    if request.method == "POST":
        # Retrieve cart data from the database with DictCursor
        cur = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM cart')
        cart_items = cur.fetchall()
        cur.close()
        
        total_cost = 0
        items = {}
        
        for key, value in request.form.items():
            if key.startswith('quantity_'):
                item_id = int(key.split('_')[1])
                quantity = int(value)
                
                # Find the corresponding item in the cart_items list
                cart_item = next((item for item in cart_items if item['medicine_id'] == item_id), None)
                
                if cart_item:
                    # Convert mrp_data to float
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT available_qty FROM medicine WHERE medicine_name = %s',(cart_item['medicine_name'],))
                    available_quantity = cur.fetchone()[0]
                    print(available_quantity)
                    cur.close()
                    if quantity > available_quantity:
                        
                        flash(f"Insufficient quantity available for {cart_item['medicine_name']}. Available quantity: {available_quantity}")
                        # Fetch all medicines for the dropdown menu
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT medicine_name FROM medicine")
                        medicines = cur.fetchall()
                        cur.close()
                        
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM cart')
                        cart_val = [dict(cart_id=row[0], customer_name=row[1], medicine_id=row[3], medicine_name=row[4], doctor_name=row[2], category_name=row[5], company_name=row[6], batch_no=row[7], mrp_data=row[8]) for row in cur.fetchall()]
                        cur.close()
                        
                        return  render_template("add_bill.html", cart_val=cart_val, medicines=medicines, message="Insufficient quantity available for {cart_item['medicine_name']}. Available quantity: {available_quantity}")
                    mrp_data = float(cart_item['mrp_data'])
                    item_cost = mrp_data * quantity  # Perform arithmetic operation
                    total_cost += item_cost

                    if item_id not in items:
                        items[item_id] = {'name': cart_item['medicine_name'], 'quantity': 0, 'cost': 0}

                    items[item_id]['quantity'] += quantity
                    items[item_id]['cost'] += item_cost
                
        total_amount = sum(item['cost'] for item in items.values())
        
        # Retrieve customer_name and doctor_name from the cart
        cur = mysql.connection.cursor()
        cur.execute('SELECT customer_name FROM cart' )
        customer_row = cur.fetchone()  # Fetch the row
        customer_name = customer_row[0] if customer_row else None
        cur.close()
          
        cur = mysql.connection.cursor()
        cur.execute('SELECT doctor_name FROM cart ')
        doctor_row = cur.fetchone()  # Fetch the row
        doctor_name = doctor_row[0] if doctor_row else None
        cur.close()
        
        # Store bill data in the database
        connection = mysql.connection
        cur = connection.cursor()
        cur.execute('INSERT INTO bill (customer_name, doctor_name, total_amount) VALUES (%s, %s, %s)', (customer_name, doctor_name, total_amount))
        bill_id = cur.lastrowid  # Retrieve the ID of the inserted bill
        connection.commit()
        
        # Store each cart item as a bill detail
        for item_id, item_data in items.items():
            # Find the corresponding item in cart_items
            cart_item = next((item for item in cart_items if item['medicine_id'] == item_id), None)
            
            # Extract the values from the cart_item or use default values if not found
            company_name = cart_item['company_name'] if cart_item else ''
            category_name = cart_item['category_name'] if cart_item else ''
            batch_no = cart_item['batch_no'] if cart_item else ''
            mrp_data = cart_item['mrp_data'] if cart_item else '' 
            cur.execute('INSERT INTO bill_details (bill_id, customer_name, doctor_name, company_name, category_name, batch_no, mrp_data, medicine_id, medicine_name, quantity, total_cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (bill_id, customer_name, doctor_name, company_name, category_name, batch_no, mrp_data, item_id, item_data['name'], item_data['quantity'], item_data['cost']))

             # Update the available quantity in the inventory
            cur.execute('UPDATE medicine SET available_qty = available_qty - %s WHERE medicine_name = %s', (item_data['quantity'], item_data['name']))

        connection.commit()
        cur.close()
        
        # Clear the cart table after processing
        cur = connection.cursor()
        cur.execute('TRUNCATE TABLE cart')
        connection.commit()
        cur.close()
        
        connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM bill WHERE bill_id = %s', (bill_id,))
        billing = [dict(bill_id=bill_id, customer_name=row[1], doctor_name=row[2], total_amount=row[3], added_on=row[4], updated_on=row[5]) for row in cursor.fetchall()]
        cursor.close()
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM bill_details WHERE bill_id = %s', (bill_id,))
        bill_details = [dict(medicine_name=row[3], quantity=row[9], mrp_data=row[8], total_cost=row[10]) for row in cursor.fetchall()]
        cursor.close()
        
        connection.close()
        return render_template('print_bill.html', billing=billing, bill_details=bill_details)
        
    else:
        return redirect(url_for('billing'))
    


@app.route('/print_bill/<int:bill_id>')
def print_bill(bill_id):
    
    connection = MySQLdb.connect(host='localhost', user='root', password='5544', database='medical_store')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM bill WHERE bill_id = %s', (bill_id,))
    billing = [dict(bill_id=bill_id, customer_name=row[1], doctor_name=row[2], total_amount=row[3], added_on=row[4], updated_on=row[5]) for row in cursor.fetchall()]
    cursor.close()
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM bill_details WHERE bill_id = %s', (bill_id,))
    bill_details = [dict(medicine_name=row[3], quantity=row[9], mrp_data=row[8], total_cost=row[10]) for row in cursor.fetchall()]
    cursor.close()
    
    connection.close()
    return render_template('print_bill.html', billing=billing, bill_details=bill_details)
    
    




    
if __name__ == "__main__":
    app.secret_key = '752d11dd239e748af53083c89950c1df'
    app.run(debug=True,port=8000)
