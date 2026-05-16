import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")

    user = "root"
    password = "latha200607"
    host = "localhost"
    port = 3306
    database_name = "userfinancetracker"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
