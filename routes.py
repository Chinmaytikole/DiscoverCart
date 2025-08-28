from flask import render_template, request, redirect, url_for, flash, jsonify, session, abort
from app import app, db
from models import Product, Section
from ai_service import generate_product_content, generate_section_description
from auth import requires_auth
import re
import json
from datetime import datetime, timezone
import os

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

@app.route('/chinmay_control_panel/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    # Check IP access first
    from auth import check_ip_access
    if not check_ip_access():
        abort(404)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        if username == admin_username and password == admin_password:
            session['admin_authenticated'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('chinmay_control_panel'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    
    return render_template('admin_login.html')

@app.route('/chinmay_control_panel/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_authenticated', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/chinmay_control_panel')
@requires_auth
def chinmay_control_panel():
    """Admin panel for managing products and sections"""
    sections = Section.query.all()
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin.html', sections=sections, products=products)

@app.route('/chinmay_control_panel/section/add', methods=['POST'])
@requires_auth
def add_section():
    """Add a new section"""
    name = request.form.get('name', '').strip()
    if not name:
        flash('Section name is required', 'error')
        return redirect(url_for('chinmay_control_panel'))
    
    slug = create_slug(name)
    
    # Check if section already exists
    if Section.query.filter_by(slug=slug).first():
        flash('Section already exists', 'error')
        return redirect(url_for('chinmay_control_panel'))
    
    # Generate description using AI
    description = generate_section_description(name)
    
    section = Section()
    section.name = name
    section.slug = slug
    section.description = description
    db.session.add(section)
    db.session.commit()
    
    flash(f'Section "{name}" added successfully!', 'success')
    return redirect(url_for('chinmay_control_panel'))

@app.route('/chinmay_control_panel/product/add', methods=['POST'])
@requires_auth
def add_product():
    """Add a new product with AI-generated content and discount"""
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        affiliate_link = request.form.get('affiliate_link', '').strip()
        section_id = request.form.get('section_id')
        price = request.form.get('price', '').strip()
        discount = request.form.get('discount_percentage', '').strip()
        image_url = request.form.get('image_url', '').strip()

        # Basic validations
        if not name or not affiliate_link or not section_id:
            flash('Product name, affiliate link, and section are required', 'error')
            return redirect(url_for('chinmay_control_panel'))

        section = Section.query.get(section_id)
        if not section:
            flash('Invalid section selected', 'error')
            return redirect(url_for('chinmay_control_panel'))

        # Generate unique slug
        slug = create_slug(name)
        counter = 1
        original_slug = slug
        while Product.query.filter_by(slug=slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1

        # Generate AI content
        flash('Generating AI content... This may take a moment.', 'info')
        ai_content = generate_product_content(name, affiliate_link, section.name, price)

        # Create product instance
        product = Product(
            name=name,
            slug=slug,
            affiliate_link=affiliate_link,
            section_id=section_id,
            price=float(price) if price else None,
            discount_percentage=float(discount) if discount else 0,
            image_url=image_url,
            short_description=ai_content['short_description'],
            full_review=ai_content['full_review'],
            pros=json.dumps(ai_content['pros']),
            cons=json.dumps(ai_content['cons']),
            seo_title=ai_content['seo_title'],
            meta_description=ai_content['meta_description']
        )

        # Save to DB
        db.session.add(product)
        db.session.commit()

        flash(f'Product "{name}" added successfully with AI-generated content!', 'success')
    
    except Exception as e:
        flash(f'Error adding product: {str(e)}', 'error')

    return redirect(url_for('chinmay_control_panel'))


@app.route('/chinmay_control_panel/product/delete/<int:product_id>', methods=['POST'])
@requires_auth
def delete_product(product_id):
    """Delete a product"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f'Product "{product.name}" deleted successfully!', 'success')
    return redirect(url_for('chinmay_control_panel'))

@app.route('/chinmay_control_panel/section/delete/<int:section_id>', methods=['POST'])
@requires_auth
def delete_section(section_id):
    """Delete a section and all its products"""
    section = Section.query.get_or_404(section_id)
    
    # Check if section has products
    if section.products:
        flash(f'Cannot delete section "{section.name}" because it contains products. Delete products first.', 'error')
        return redirect(url_for('chinmay_control_panel'))
    
    db.session.delete(section)
    db.session.commit()
    flash(f'Section "{section.name}" deleted successfully!', 'success')
    return redirect(url_for('chinmay_control_panel'))

# Add these new routes to your existing routes.py file

@app.route('/chinmay_control_panel/product/edit/<int:product_id>', methods=['GET'])
@requires_auth
def edit_product_form(product_id):
    """Show product edit form"""
    product = Product.query.get_or_404(product_id)
    sections = Section.query.all()
    
    # Parse pros and cons from JSON strings for editing
    try:
        pros = json.loads(product.pros) if product.pros else []
        cons = json.loads(product.cons) if product.cons else []
    except:
        pros = []
        cons = []
    
    return render_template('edit_product.html', 
                         product=product, 
                         sections=sections, 
                         pros=pros, 
                         cons=cons)

@app.route('/chinmay_control_panel/product/update/<int:product_id>', methods=['POST'])
@requires_auth
def update_product(product_id):
    """Update existing product"""
    product = Product.query.get_or_404(product_id)
    
    name = request.form.get('name', '').strip()
    affiliate_link = request.form.get('affiliate_link', '').strip()
    section_id = request.form.get('section_id')
    price = request.form.get('price', '').strip()
    image_url = request.form.get('image_url', '').strip()
    discount_percentage = request.form.get('discount_percentage', '').strip()
    
    # Manual content fields (optional - user can edit AI content)
    short_description = request.form.get('short_description', '').strip()
    full_review = request.form.get('full_review', '').strip()
    seo_title = request.form.get('seo_title', '').strip()
    meta_description = request.form.get('meta_description', '').strip()
    
    # Pros and cons as comma-separated values
    pros_text = request.form.get('pros', '').strip()
    cons_text = request.form.get('cons', '').strip()
    
    # Check if regenerate AI content is requested
    regenerate_ai = request.form.get('regenerate_ai') == 'on'
    
    if not name or not affiliate_link or not section_id:
        flash('Product name, affiliate link, and section are required', 'error')
        return redirect(url_for('edit_product_form', product_id=product_id))
    
    section = Section.query.get(section_id)
    if not section:
        flash('Invalid section selected', 'error')
        return redirect(url_for('edit_product_form', product_id=product_id))
    
    try:
        # Update basic product info
        product.name = name
        product.affiliate_link = affiliate_link
        product.section_id = section_id
        product.price = price
        product.image_url = image_url
        
        # Handle discount percentage
        if discount_percentage:
            try:
                product.discount_percentage = float(discount_percentage)
            except ValueError:
                product.discount_percentage = 0.0
        else:
            product.discount_percentage = 0.0
        
        # Update slug if name changed
        new_slug = create_slug(name)
        if new_slug != product.slug:
            counter = 1
            original_slug = new_slug
            
            # Ensure unique slug
            while Product.query.filter(Product.slug == new_slug, Product.id != product_id).first():
                new_slug = f"{original_slug}-{counter}"
                counter += 1
            
            product.slug = new_slug
        
        # Handle AI content regeneration or manual updates
        if regenerate_ai:
            flash('Regenerating AI content... This may take a moment.', 'info')
            ai_content = generate_product_content(name, affiliate_link, section.name, price)
            
            product.short_description = ai_content['short_description']
            product.full_review = ai_content['full_review']
            product.pros = json.dumps(ai_content['pros'])
            product.cons = json.dumps(ai_content['cons'])
            product.seo_title = ai_content['seo_title']
            product.meta_description = ai_content['meta_description']
            
            flash(f'Product "{name}" updated with new AI-generated content!', 'success')
        else:
            # Update with manual content if provided
            if short_description:
                product.short_description = short_description
            if full_review:
                product.full_review = full_review
            if seo_title:
                product.seo_title = seo_title
            if meta_description:
                product.meta_description = meta_description
            
            # Handle pros and cons
            if pros_text:
                pros_list = [p.strip() for p in pros_text.split(',') if p.strip()]
                product.pros = json.dumps(pros_list)
            
            if cons_text:
                cons_list = [c.strip() for c in cons_text.split(',') if c.strip()]
                product.cons = json.dumps(cons_list)
            
            flash(f'Product "{name}" updated successfully!', 'success')
        
        # Update timestamp
        product.updated_at = datetime.now(timezone.utc)
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating product: {str(e)}', 'error')
        return redirect(url_for('edit_product_form', product_id=product_id))
    
    return redirect(url_for('chinmay_control_panel'))

@app.route('/chinmay_control_panel/product/quick-edit/<int:product_id>', methods=['POST'])
@requires_auth
def quick_edit_product(product_id):
    """Quick edit for basic product info via AJAX"""
    product = Product.query.get_or_404(product_id)
    
    field = request.form.get('field')
    value = request.form.get('value', '').strip()
    
    try:
        if field == 'name':
            product.name = value
            # Update slug if name changed
            new_slug = create_slug(value)
            counter = 1
            original_slug = new_slug
            
            while Product.query.filter(Product.slug == new_slug, Product.id != product_id).first():
                new_slug = f"{original_slug}-{counter}"
                counter += 1
            
            product.slug = new_slug
            
        elif field == 'price':
            product.price = value
        elif field == 'affiliate_link':
            product.affiliate_link = value
        elif field == 'image_url':
            product.image_url = value
        elif field == 'discount_percentage':
            product.discount_percentage = float(value) if value else 0.0
        else:
            return jsonify({'success': False, 'error': 'Invalid field'})
        
        # Update timestamp
        product.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'{field.title()} updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

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
