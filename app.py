from flask import Flask, render_template
from config import Config
from extensions import db, bcrypt, migrate, login_manager
from api import register_apis
from models import User
from flask_login import logout_user, login_required

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

login_manager.login_view = 'login'

# Register APIs
register_apis(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ── HTML Routes ──
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/transactions')
@login_required
def transactions():
    return render_template('transactions.html')

@app.route('/budgets')
@login_required
def budgets():
    return render_template('budgets.html')

@app.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')

@app.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)