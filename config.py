import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    database_name = os.getenv("DB_NAME")
    SECRET_KEY = 'your_secret_key_here'

    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost/userfinancetracker"
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost/userfinancetracker"
    user = "root"
    password = "password"
    host = "localhost"
    port = "3306"
    database_name = "userfinancetracker"
    SQLALCHEMY_DATABASE_URI = f"mysql://{user}:{password}@{host}:{port}/{database_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False