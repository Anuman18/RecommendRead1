import os
import logging
from flask import Flask, jsonify

from flask_cors import CORS
from extensions import db

# Setup logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create base class for SQLAlchemy models

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# ✅ Use SQLite database (file-based, local)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///recommread.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# ✅ Optional: skip PostgreSQL-specific engine options
# You can remove this block or keep it empty
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}

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

    # Import web blueprint
    from routes.web import web_bp

    # Register API blueprints with proper URL prefixes
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(stories_bp, url_prefix='/api')
    app.register_blueprint(bookmarks_bp, url_prefix='/api')

    # Register web blueprint for frontend
    app.register_blueprint(web_bp)

    # Add a simple API status check route
    @app.route('/api')
    def api_status():
        return jsonify({
            'status': 'online',
            'app': 'RecommRead API',
            'version': '1.0.0'
        })

if __name__ == "__main__":
    app.run(debug=True)
