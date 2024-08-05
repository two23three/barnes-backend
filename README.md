# Barnes

config.py: Contains configuration settings.

models.py: Defines your SQLAlchemy models.

app.py: Initializes the Flask app and sets up Flask-Admin.

init_db.py: Initializes the database schema.

requirements.txt: Lists dependencies for easy installation.

## Steps to Run Your Application

1. Set Up Your Environment

    Make sure your virtual environment is active.

    ``` bash
    source venv/bin/activate
    ```

2. Install Dependencies

    Install the required packages listed in requirements.txt.

    ```bash
    pip install -r requirements.txt
    ```

3. Initialize the Database

    Run init_db.py to create the database tables.

    ```bash
    python init_db.py
    ```

4. Run the Flask Application

    Start your Flask application.

    ```bash
    python app.py
    ```
