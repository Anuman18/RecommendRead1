import os
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import DeclarativeBase

# Setup logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with our base class
db = SQLAlchemy(model_class=Base)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure database to use PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Enable CORS for frontend compatibility
CORS(app)

# Initialize the database with the app
db.init_app(app)

# Import and register routes
with app.app_context():
    # Import models first to ensure they're defined before creating tables
    from models import User, Story, Bookmark
    
    # Create all tables
    db.create_all()
    
    # Import and register blueprint routes
    from routes.auth import auth_bp
    from routes.stories import stories_bp
    from routes.bookmarks import bookmarks_bp
    
    # Register blueprints with proper URL prefixes
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(stories_bp, url_prefix='/api')
    app.register_blueprint(bookmarks_bp, url_prefix='/api')
    
    # Add a root route for API status check
    @app.route('/')
    def index():
        return jsonify({
            'status': 'online',
            'app': 'RecommRead API',
            'version': '1.0.0'
        })
