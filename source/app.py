# app.py

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User
import config

app = Flask(__name__)
app.config.from_object(config.Config)

# Initialize extensions
db.init_app(app)
admin = Admin(app, name='MyApp', template_mode='bootstrap3')

# Add model views to Flask-Admin
admin.add_view(ModelView(User, db.session))

@app.route('/')
def index():
    return "Welcome to BizzGogo!"

if __name__ == '__main__':
    app.run(debug=True)