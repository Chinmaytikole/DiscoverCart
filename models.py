from app import db
from datetime import datetime
from sqlalchemy import func

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with products
    products = db.relationship('Product', backref='section', lazy=True, cascade='all, delete-orphan')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    affiliate_link = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(50))
    image_url = db.Column(db.Text)
    
    # AI Generated Content
    short_description = db.Column(db.Text)
    full_review = db.Column(db.Text)
    pros = db.Column(db.Text)  # JSON string of pros list
    cons = db.Column(db.Text)  # JSON string of cons list
    seo_title = db.Column(db.String(200))
    meta_description = db.Column(db.Text)
    
    # Relationships
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Search functionality
    @classmethod
    def search(cls, query):
        return cls.query.filter(
            db.or_(
                cls.name.contains(query),
                cls.short_description.contains(query),
                cls.full_review.contains(query)
            )
        ).all()
