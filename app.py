import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Optional: load .env for local development
from dotenv import load_dotenv
load_dotenv()

# Define SQLAlchemy Base
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with custom Base
db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Fix for proxy headers (important when behind Render's proxy)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Choose database URI depending on environment
# Use PostgreSQL on Render, SQLite locally
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    # Render gives old-style URL; SQLAlchemy needs "postgresql://"
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///affiliate_site.db"

# Optional database engine configs
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize app with SQLAlchemy
db.init_app(app)

# App context setup: models, routes, and DB table creation
with app.app_context():
    import models  # ensure models are loaded
    import routes  # register routes
    db.create_all()  # create tables if they don't exist

# Global template context
@app.context_processor
def inject_sections():
    from models import Section
    sections = Section.query.all()
    return dict(sections=sections)

# Start development server (not used in production — Render uses gunicorn)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
