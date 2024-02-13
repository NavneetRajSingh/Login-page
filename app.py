from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
import re

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Navneet@2110'
app.config['MYSQL_DB'] = 'devzery_assignment'
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

# MySQL database connection
mysql = MySQL(app)
cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

class User(UserMixin):
    def __init__(self, id, username, email, is_verified=False):
        self.id = id
        self.username = username
        self.email = email
        self.is_verified = is_verified

@login_manager.user_loader
def load_user(user_id):
    return User(int(user_id))
def register():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        else:
            hashed_password = password.encode('utf-8').hexdigest()
            cursor.execute("INSERT INTO users (username, email, password, is_verified) VALUES (%s, %s, %s, %s)", (username, email, hashed_password, 0))
            mysql.connection.commit()
            message = 'You have successfully registered!'
    return render_template('register.html', message=message)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email = %s AND is_verified = 1", (email,))
        user = cursor.fetchone()
        if user:
            if user['password'] == hashed_password:
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect password. Please try again.')
        else:
            flash('No account with this email. Please register.')
    return render_template('login.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

if __name__ == "__main__":
    app.run(debug=True)