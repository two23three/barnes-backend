import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://mike:nU6Li3vmuDYEQptTz86PNMhOsaYCqNKu@dpg-cqlljsg8fa8c73b454k0-a.oregon-postgres.render.com/mydatabase_0nn3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
