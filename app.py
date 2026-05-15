from flask import Flask
from config import Config
from extensions import db, bcrypt, migrate, login_manager
from api import register_apis

def create_app():
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

    return app


# 👇 THIS LINE IS THE KEY FIX
app = create_app()


if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)