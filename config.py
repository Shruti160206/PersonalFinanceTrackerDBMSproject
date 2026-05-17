import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")

    user = "root"
    password = os.getenv("DB_PASSWORD", "password")
    host = "localhost"
    port = 3306
    database_name = "userfinancetracker"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
