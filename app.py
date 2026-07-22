import os

from flask import Flask, request, redirect, url_for, render_template_string, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'ABCD123456789' 

DATABASE_URL = os.getenv('DATABASE_URL') or "postgresql://postgres:@db.klahrymtwhwltigfeltp.supabase.co:5432/postgres" #ACu1iRjHrJmXjVHx
if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    pg_user = os.getenv('POSTGRES_USER', 'postgres')
    pg_pass = os.getenv('POSTGRES_PASSWORD', 'postgres')
    pg_host = os.getenv('POSTGRES_HOST', 'localhost')
    pg_port = os.getenv('POSTGRES_PORT', '5432')
    pg_db = os.getenv('POSTGRES_DB', 'users_db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:ACu1iRjHrJmXjVHx@db.klahrymtwhwltigfeltp.supabase.co:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('profile'))
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        name = request.form.get('name', '').strip()

        if not username or not password or not name:
            return render_template_string('''
                <h2>Signup</h2>
                <p>Please enter name, username and password.</p>
                <form method="post">
                    <input name="name" placeholder="Full Name"><br><br>
                    <input name="username" placeholder="Username"><br><br>
                    <input name="password" type="password" placeholder="Password"><br><br>
                    <button type="submit">Sign Up</button>
                </form>
                <p><a href="/login">Already have an account? Login</a></p>
            ''')

        if User.query.filter_by(username=username).first():
            return render_template_string('''
                <h2>Signup</h2>
                <p>Username already exists.</p>
                <form method="post">
                    <input name="name" placeholder="Full Name"><br><br>
                    <input name="username" placeholder="Username"><br><br>
                    <input name="password" type="password" placeholder="Password"><br><br>
                    <button type="submit">Sign Up</button>
                </form>
                <p><a href="/login">Already have an account? Login</a></p>
            ''')

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, name=name)
        db.session.add(new_user)
        db.session.commit()
        
        session['user'] = username
        return redirect(url_for('profile'))

    return render_template_string('''
        <h2>Signup</h2>
        <form method="post">
            <input name="name" placeholder="Full Name"><br><br>
            <input name="username" placeholder="Username"><br><br>
            <input name="password" type="password" placeholder="Password"><br><br>
            <button type="submit">Sign Up</button>
        </form>
        <p><a href="/login">Already have an account? Login</a></p>
    ''')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = username
            return redirect(url_for('profile'))

        return render_template_string('''
            <h2>Login</h2>
            <p>Invalid username or password.</p>
            <form method="post">
                <input name="username" placeholder="Username"><br><br>
                <input name="password" type="password" placeholder="Password"><br><br>
                <button type="submit">Login</button>
            </form>
            <p><a href="/signup">Create an account</a></p>
        ''')

    return render_template_string('''
        <h2>Login</h2>
        <form method="post">
            <input name="username" placeholder="Username"><br><br>
            <input name="password" type="password" placeholder="Password"><br><br>
            <button type="submit">Login</button>
        </form>
        <p><a href="/signup">Create an account</a></p>
    ''')


@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['user']).first()
    if not user:
        return redirect(url_for('login'))
    
    return render_template_string('''
        <h2>Profile</h2>
        <p>Welcome, {{ name }}!</p>
        <p>Username: {{ username }}</p>
        <p>This is your profile page.</p>
        <a href="/logout">Logout</a>
    ''', name=user.name, username=user.username)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
