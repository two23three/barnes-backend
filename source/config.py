import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://barnes:yC4zayEqMLQCSgoCnSqv6GnqOZbhX4Bm@dpg-cqpl5d3v2p9s73cei9rg-a.oregon-postgres.render.com/barnes')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
