import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://barnes:0Ad8Zot1vAb8JTHAoFAq3fFwxNmt4vm3@dpg-cqsrfvlsvqrc73flpjh0-a.oregon-postgres.render.com/barnes_97j7')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','postgresql://postgres:newpassword@localhost/mydatabase')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
