from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Product, Section
from ai_service import generate_product_content, generate_section_description
import re
import json

def create_slug(text):
    """Create URL-friendly slug from text"""
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

@app.route('/')
def index():
    """Homepage showing featured products and sections"""
    sections = Section.query.all()
    featured_products = Product.query.order_by(Product.created_at.desc()).limit(6).all()
    return render_template('index.html', sections=sections, featured_products=featured_products)

@app.route('/section/<slug>')
def section_view(slug):
    """View products in a specific section"""
    section = Section.query.filter_by(slug=slug).first_or_404()
    products = Product.query.filter_by(section_id=section.id).order_by(Product.created_at.desc()).all()
    return render_template('section.html', section=section, products=products)

@app.route('/product/<slug>')
def product_view(slug):
    """View individual product details"""
    product = Product.query.filter_by(slug=slug).first_or_404()
    
    # Parse pros and cons from JSON strings
    try:
        pros = json.loads(product.pros) if product.pros else []
        cons = json.loads(product.cons) if product.cons else []
    except:
        pros = []
        cons = []
    
    return render_template('product.html', product=product, pros=pros, cons=cons)

@app.route('/search')
def search():
    """Search products"""
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('index'))
    
    products = Product.search(query)
    return render_template('section.html', 
                         section={'name': f'Search Results for "{query}"', 'description': f'Found {len(products)} products matching your search.'}, 
                         products=products)

@app.route('/admin')
def admin():
    """Admin panel for managing products and sections"""
    sections = Section.query.all()
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin.html', sections=sections, products=products)

@app.route('/admin/section/add', methods=['POST'])
def add_section():
    """Add a new section"""
    name = request.form.get('name', '').strip()
    if not name:
        flash('Section name is required', 'error')
        return redirect(url_for('admin'))
    
    slug = create_slug(name)
    
    # Check if section already exists
    if Section.query.filter_by(slug=slug).first():
        flash('Section already exists', 'error')
        return redirect(url_for('admin'))
    
    # Generate description using AI
    description = generate_section_description(name)
    
    section = Section()
    section.name = name
    section.slug = slug
    section.description = description
    db.session.add(section)
    db.session.commit()
    
    flash(f'Section "{name}" added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/product/add', methods=['POST'])
def add_product():
    """Add a new product with AI-generated content"""
    name = request.form.get('name', '').strip()
    affiliate_link = request.form.get('affiliate_link', '').strip()
    section_id = request.form.get('section_id')
    price = request.form.get('price', '').strip()
    image_url = request.form.get('image_url', '').strip()
    
    if not name or not affiliate_link or not section_id:
        flash('Product name, affiliate link, and section are required', 'error')
        return redirect(url_for('admin'))
    
    section = Section.query.get(section_id)
    if not section:
        flash('Invalid section selected', 'error')
        return redirect(url_for('admin'))
    
    slug = create_slug(name)
    counter = 1
    original_slug = slug
    
    # Ensure unique slug
    while Product.query.filter_by(slug=slug).first():
        slug = f"{original_slug}-{counter}"
        counter += 1
    
    try:
        # Generate AI content
        flash('Generating AI content... This may take a moment.', 'info')
        ai_content = generate_product_content(name, affiliate_link, section.name, price)
        
        # Create product
        product = Product()
        product.name = name
        product.slug = slug
        product.affiliate_link = affiliate_link
        product.section_id = section_id
        product.price = price
        product.image_url = image_url
        product.short_description = ai_content['short_description']
        product.full_review = ai_content['full_review']
        product.pros = json.dumps(ai_content['pros'])
        product.cons = json.dumps(ai_content['cons'])
        product.seo_title = ai_content['seo_title']
        product.meta_description = ai_content['meta_description']
        
        db.session.add(product)
        db.session.commit()
        
        flash(f'Product "{name}" added successfully with AI-generated content!', 'success')
        
    except Exception as e:
        flash(f'Error adding product: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    """Delete a product"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f'Product "{product.name}" deleted successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/section/delete/<int:section_id>', methods=['POST'])
def delete_section(section_id):
    """Delete a section and all its products"""
    section = Section.query.get_or_404(section_id)
    
    # Check if section has products
    if section.products:
        flash(f'Cannot delete section "{section.name}" because it contains products. Delete products first.', 'error')
        return redirect(url_for('admin'))
    
    db.session.delete(section)
    db.session.commit()
    flash(f'Section "{section.name}" deleted successfully!', 'success')
    return redirect(url_for('admin'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    sections = Section.query.all()
    return render_template('base.html', sections=sections), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    sections = Section.query.all()
    return render_template('base.html', sections=sections), 500
