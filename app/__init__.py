from flask import Flask

def create_app():
    app = Flask(__name__)
    # Import and register blueprints here if needed
    return app
