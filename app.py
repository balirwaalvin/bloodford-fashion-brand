import os
import secrets
from datetime import datetime, timedelta
from functools import wraps
import json
import random
import string

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# ── App Configuration ────────────────────────────────────────────────
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloodford_fashion.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# ══════════════════════════════════════════════════════════════════════
# DATABASE MODELS
# ══════════════════════════════════════════════════════════════════════

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(300), default='')
    city = db.Column(db.String(100), default='')
    country = db.Column(db.String(100), default='')
    profile_pic = db.Column(db.String(200), default='default.png')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True)
    wishlist = db.relationship('Wishlist', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float, nullable=True)
    category = db.Column(db.String(50), nullable=False)  # men, women, unisex
    subcategory = db.Column(db.String(50), nullable=False)
    sizes = db.Column(db.String(200), default='S,M,L,XL,XXL')
    colors = db.Column(db.String(200), default='Black,White,Red')
    image = db.Column(db.String(300), nullable=False)
    image2 = db.Column(db.String(300), default='')
    image3 = db.Column(db.String(300), default='')
    stock = db.Column(db.Integer, default=50)
    featured = db.Column(db.Boolean, default=False)
    new_arrival = db.Column(db.Boolean, default=False)
    best_seller = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=4.5)
    num_reviews = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    size = db.Column(db.String(10), default='M')
    color = db.Column(db.String(30), default='Black')
    added_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    shipping_fee = db.Column(db.Float, default=5000.0)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    order_status = db.Column(db.String(30), default='processing')  # processing, confirmed, shipped, in_transit, out_for_delivery, delivered
    shipping_address = db.Column(db.String(300), nullable=False)
    shipping_city = db.Column(db.String(100), nullable=False)
    shipping_country = db.Column(db.String(100), nullable=False)
    tracking_number = db.Column(db.String(30), default='')
    estimated_delivery = db.Column(db.DateTime, nullable=True)
    shipped_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text, default='')

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    tracking_updates = db.relationship('TrackingUpdate', backref='order', lazy=True, cascade='all, delete-orphan')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(10))
    color = db.Column(db.String(30))
    price = db.Column(db.Float, nullable=False)


class TrackingUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), default='')
    description = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', backref='wishlisted_by')


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ── Helper Functions ─────────────────────────────────────────────────

def generate_order_number():
    prefix = 'PC'
    timestamp = datetime.utcnow().strftime('%y%m%d')
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f'{prefix}-{timestamp}-{random_part}'


def generate_tracking_number():
    return 'TRK' + ''.join(random.choices(string.digits, k=12))


def simulate_tracking_updates(order):
    """Simulate tracking updates for an order"""
    statuses = [
        ('processing', 'Warehouse', 'Order is being processed and prepared for shipping.'),
        ('confirmed', 'Warehouse', 'Order has been confirmed and packaged.'),
        ('shipped', 'Distribution Center', 'Package has been shipped from our distribution center.'),
        ('in_transit', 'Transit Hub', 'Package is in transit to your city.'),
        ('out_for_delivery', order.shipping_city, 'Package is out for delivery in your area.'),
        ('delivered', order.shipping_address, 'Package has been delivered successfully!')
    ]

    status_index = ['processing', 'confirmed', 'shipped', 'in_transit', 'out_for_delivery', 'delivered']
    current_index = status_index.index(order.order_status) if order.order_status in status_index else 0

    for i in range(current_index + 1):
        existing = TrackingUpdate.query.filter_by(
            order_id=order.id, status=statuses[i][0]
        ).first()
        if not existing:
            update = TrackingUpdate(
                order_id=order.id,
                status=statuses[i][0],
                location=statuses[i][1],
                description=statuses[i][2],
                timestamp=order.created_at + timedelta(hours=i * 12 + random.randint(1, 6))
            )
            db.session.add(update)

    db.session.commit()


def get_cart_count():
    if current_user.is_authenticated:
        return CartItem.query.filter_by(user_id=current_user.id).count()
    return 0


@app.context_processor
def inject_cart_count():
    return dict(cart_count=get_cart_count())


# ══════════════════════════════════════════════════════════════════════
# PUBLIC ROUTES
# ══════════════════════════════════════════════════════════════════════

@app.route('/')
def home():
    featured = Product.query.filter_by(featured=True).limit(8).all()
    new_arrivals = Product.query.filter_by(new_arrival=True).limit(4).all()
    best_sellers = Product.query.filter_by(best_seller=True).limit(4).all()
    return render_template('home.html', featured=featured, new_arrivals=new_arrivals, best_sellers=best_sellers)


@app.route('/shop')
def shop():
    category = request.args.get('category', 'all')
    subcategory = request.args.get('subcategory', 'all')
    sort = request.args.get('sort', 'newest')
    search = request.args.get('search', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    page = request.args.get('page', 1, type=int)

    query = Product.query

    if category != 'all':
        query = query.filter_by(category=category)
    if subcategory != 'all':
        query = query.filter_by(subcategory=subcategory)
    if search:
        query = query.filter(
            db.or_(
                Product.name.ilike(f'%{search}%'),
                Product.description.ilike(f'%{search}%')
            )
        )
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)

    if sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort == 'rating':
        query = query.order_by(Product.rating.desc())
    elif sort == 'popular':
        query = query.order_by(Product.best_seller.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    products = query.paginate(page=page, per_page=12, error_out=False)
    return render_template('shop.html', products=products, category=category, subcategory=subcategory, sort=sort, search=search)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id
    ).limit(4).all()
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    return render_template('product_detail.html', product=product, related=related, reviews=reviews)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for your message! We will get back to you shortly.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')


# ══════════════════════════════════════════════════════════════════════
# AUTH ROUTES
# ══════════════════════════════════════════════════════════════════════

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not all([first_name, last_name, email, phone, password]):
            flash('All fields are required.', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('login'))

        user = User(first_name=first_name, last_name=last_name, email=email, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f'Welcome to Peter\'s Collection, {first_name}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=bool(remember))
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(next_page or url_for('home'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


# ══════════════════════════════════════════════════════════════════════
# CART ROUTES
# ══════════════════════════════════════════════════════════════════════

@app.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(item.product.price * item.quantity for item in items)
    shipping = 5000.0 if items else 0
    total = subtotal + shipping
    return render_template('cart.html', items=items, subtotal=subtotal, shipping=shipping, total=total)


@app.route('/api/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    size = data.get('size', 'M')
    color = data.get('color', 'Black')

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found.'}), 404

    existing = CartItem.query.filter_by(
        user_id=current_user.id, product_id=product_id, size=size, color=color
    ).first()

    if existing:
        existing.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id, product_id=product_id,
            quantity=quantity, size=size, color=color
        )
        db.session.add(cart_item)

    db.session.commit()
    count = CartItem.query.filter_by(user_id=current_user.id).count()
    return jsonify({'success': True, 'message': 'Added to cart!', 'cart_count': count})


@app.route('/api/cart/update', methods=['POST'])
@login_required
def update_cart():
    data = request.get_json()
    item_id = data.get('item_id')
    quantity = data.get('quantity', 1)

    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        return jsonify({'success': False, 'message': 'Item not found.'}), 404

    if quantity <= 0:
        db.session.delete(item)
    else:
        item.quantity = quantity

    db.session.commit()

    items = CartItem.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(i.product.price * i.quantity for i in items)
    shipping = 5000.0 if items else 0
    total = subtotal + shipping
    count = len(items)

    return jsonify({
        'success': True,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'cart_count': count
    })


@app.route('/api/cart/remove', methods=['POST'])
@login_required
def remove_from_cart():
    data = request.get_json()
    item_id = data.get('item_id')

    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if item:
        db.session.delete(item)
        db.session.commit()

    count = CartItem.query.filter_by(user_id=current_user.id).count()
    return jsonify({'success': True, 'cart_count': count})


# ══════════════════════════════════════════════════════════════════════
# WISHLIST ROUTES
# ══════════════════════════════════════════════════════════════════════

@app.route('/wishlist')
@login_required
def wishlist():
    items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', items=items)


@app.route('/api/wishlist/toggle', methods=['POST'])
@login_required
def toggle_wishlist():
    data = request.get_json()
    product_id = data.get('product_id')

    existing = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'success': True, 'action': 'removed', 'message': 'Removed from wishlist.'})
    else:
        item = Wishlist(user_id=current_user.id, product_id=product_id)
        db.session.add(item)
        db.session.commit()
        return jsonify({'success': True, 'action': 'added', 'message': 'Added to wishlist!'})


# ══════════════════════════════════════════════════════════════════════
# CHECKOUT & PAYMENT ROUTES
# ══════════════════════════════════════════════════════════════════════

@app.route('/checkout')
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('shop'))

    subtotal = sum(item.product.price * item.quantity for item in items)
    shipping = 5000.0
    total = subtotal + shipping
    return render_template('checkout.html', items=items, subtotal=subtotal, shipping=shipping, total=total)


@app.route('/api/place-order', methods=['POST'])
@login_required
def place_order():
    data = request.get_json()

    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        return jsonify({'success': False, 'message': 'Cart is empty.'}), 400

    subtotal = sum(item.product.price * item.quantity for item in items)
    shipping = 5000.0
    total = subtotal + shipping

    order = Order(
        user_id=current_user.id,
        order_number=generate_order_number(),
        total_amount=total,
        shipping_fee=shipping,
        payment_method=data.get('payment_method', 'mobile_money'),
        payment_status='completed',  # Simulated payment
        order_status='processing',
        shipping_address=data.get('address', current_user.address),
        shipping_city=data.get('city', current_user.city),
        shipping_country=data.get('country', current_user.country),
        tracking_number=generate_tracking_number(),
        estimated_delivery=datetime.utcnow() + timedelta(days=random.randint(5, 10)),
        notes=data.get('notes', '')
    )
    db.session.add(order)
    db.session.flush()

    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            size=item.size,
            color=item.color,
            price=item.product.price
        )
        db.session.add(order_item)

        # Reduce stock
        product = Product.query.get(item.product_id)
        if product:
            product.stock = max(0, product.stock - item.quantity)

    # Add initial tracking update
    tracking = TrackingUpdate(
        order_id=order.id,
        status='processing',
        location='Warehouse',
        description='Order received and is being processed.',
        timestamp=datetime.utcnow()
    )
    db.session.add(tracking)

    # Clear cart
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    return jsonify({
        'success': True,
        'order_number': order.order_number,
        'message': 'Order placed successfully!'
    })


@app.route('/payment-success/<order_number>')
@login_required
def payment_success(order_number):
    order = Order.query.filter_by(order_number=order_number, user_id=current_user.id).first_or_404()
    return render_template('payment_success.html', order=order)


# ══════════════════════════════════════════════════════════════════════
# ORDER & TRACKING ROUTES
# ══════════════════════════════════════════════════════════════════════

@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)


@app.route('/track/<order_number>')
@login_required
def track_order(order_number):
    order = Order.query.filter_by(order_number=order_number, user_id=current_user.id).first_or_404()

    # Simulate order progression
    status_flow = ['processing', 'confirmed', 'shipped', 'in_transit', 'out_for_delivery', 'delivered']
    current_idx = status_flow.index(order.order_status) if order.order_status in status_flow else 0

    # Auto-advance order status for demo purposes (advance by 1 step each visit, max 1 per 10 sec)
    if current_idx < len(status_flow) - 1:
        last_update = TrackingUpdate.query.filter_by(order_id=order.id).order_by(TrackingUpdate.timestamp.desc()).first()
        if last_update and (datetime.utcnow() - last_update.timestamp).total_seconds() > 10:
            next_status = status_flow[current_idx + 1]
            order.order_status = next_status

            location_map = {
                'confirmed': 'Warehouse',
                'shipped': 'Distribution Center',
                'in_transit': 'Transit Hub - En route',
                'out_for_delivery': order.shipping_city,
                'delivered': order.shipping_address
            }
            desc_map = {
                'confirmed': 'Your order has been confirmed and is being prepared.',
                'shipped': 'Your package has been shipped from our distribution center.',
                'in_transit': 'Your package is currently in transit.',
                'out_for_delivery': 'Your package is out for delivery!',
                'delivered': 'Your package has been delivered. Enjoy!'
            }

            update = TrackingUpdate(
                order_id=order.id,
                status=next_status,
                location=location_map.get(next_status, ''),
                description=desc_map.get(next_status, ''),
                timestamp=datetime.utcnow()
            )
            db.session.add(update)

            if next_status == 'shipped':
                order.shipped_at = datetime.utcnow()
            elif next_status == 'delivered':
                order.delivered_at = datetime.utcnow()

            db.session.commit()

    tracking_updates = TrackingUpdate.query.filter_by(order_id=order.id).order_by(TrackingUpdate.timestamp.desc()).all()

    # Calculate delivery countdown
    remaining = None
    if order.estimated_delivery and order.order_status != 'delivered':
        remaining = order.estimated_delivery - datetime.utcnow()
        if remaining.total_seconds() < 0:
            remaining = timedelta(0)

    return render_template('tracking.html', order=order, tracking_updates=tracking_updates, remaining=remaining)


# ══════════════════════════════════════════════════════════════════════
# PROFILE ROUTES
# ══════════════════════════════════════════════════════════════════════

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name', current_user.first_name)
        current_user.last_name = request.form.get('last_name', current_user.last_name)
        current_user.phone = request.form.get('phone', current_user.phone)
        current_user.address = request.form.get('address', '')
        current_user.city = request.form.get('city', '')
        current_user.country = request.form.get('country', '')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html')


# ══════════════════════════════════════════════════════════════════════
# REVIEW ROUTES
# ══════════════════════════════════════════════════════════════════════

@app.route('/api/review', methods=['POST'])
@login_required
def add_review():
    data = request.get_json()
    product_id = data.get('product_id')
    rating = data.get('rating', 5)
    comment = data.get('comment', '')

    existing = Review.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        return jsonify({'success': False, 'message': 'You have already reviewed this product.'}), 400

    review = Review(user_id=current_user.id, product_id=product_id, rating=rating, comment=comment)
    db.session.add(review)

    # Update product rating
    product = Product.query.get(product_id)
    if product:
        all_reviews = Review.query.filter_by(product_id=product_id).all()
        product.num_reviews = len(all_reviews) + 1
        product.rating = round(sum(r.rating for r in all_reviews + [review]) / (len(all_reviews) + 1), 1)

    db.session.commit()
    return jsonify({'success': True, 'message': 'Review submitted!'})


# ══════════════════════════════════════════════════════════════════════
# NEWSLETTER
# ══════════════════════════════════════════════════════════════════════

@app.route('/api/newsletter', methods=['POST'])
def subscribe_newsletter():
    data = request.get_json()
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({'success': False, 'message': 'Email is required.'}), 400

    if Newsletter.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'Already subscribed!'}), 400

    sub = Newsletter(email=email)
    db.session.add(sub)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Subscribed successfully!'})


# ══════════════════════════════════════════════════════════════════════
# SEED DATA
# ══════════════════════════════════════════════════════════════════════

def seed_products():
    if Product.query.first():
        return

    products = [
        # ── Men's Collection ─────────────────────────────────────────
        Product(name="Classic Black Tailored Suit", description="Impeccably tailored black suit crafted from premium wool blend. Features a modern slim-fit silhouette with notch lapels, functioning buttonholes, and a fully lined interior. Perfect for business meetings and formal events. A BloodFord Fashion Brand original.", price=285000, original_price=350000, category="men", subcategory="suits", image="suit_black.jpg", featured=True, best_seller=True, rating=4.8, num_reviews=124),
        Product(name="Red Power Blazer", description="Make a bold statement with this striking red blazer. Designed with a contemporary fit, peak lapels, and contrast black lining. Pairs beautifully with dark trousers for a look that commands attention. Exclusively designed by BloodFord Fashion Brand.", price=175000, original_price=220000, category="men", subcategory="blazers", image="blazer_red.jpg", featured=True, new_arrival=True, rating=4.7, num_reviews=89),
        Product(name="Crisp White Oxford Shirt", description="The essential white shirt reimagined. Made from Egyptian cotton with a subtle texture, featuring a spread collar and adjustable cuffs. A versatile piece that transitions effortlessly from office to evening. Original BloodFord Fashion Brand design.", price=65000, category="men", subcategory="shirts", image="shirt_white.jpg", featured=True, best_seller=True, rating=4.9, num_reviews=203),
        Product(name="Black Slim-Fit Chinos", description="Elevated everyday wear in jet black. These slim-fit chinos feature a comfortable stretch fabric, clean front design, and tapered leg. The perfect foundation for any outfit. BloodFord Fashion Brand craftsmanship.", price=85000, original_price=95000, category="men", subcategory="trousers", image="chinos_black.jpg", best_seller=True, rating=4.6, num_reviews=156),
        Product(name="Red & Black Bomber Jacket", description="Urban sophistication meets bold design. This bomber jacket features a striking red and black colorblock pattern, ribbed cuffs and hem, and premium satin lining. A BloodFord Fashion Brand street-style essential.", price=145000, category="men", subcategory="jackets", image="bomber_rb.jpg", new_arrival=True, featured=True, rating=4.7, num_reviews=67),
        Product(name="Monochrome Polo Collection", description="Effortless style in a classic polo design. Made from premium piqué cotton with the signature BloodFord Fashion Brand emblem. Available in black, white, and red. The ultimate casual luxury piece.", price=55000, category="men", subcategory="polos", image="polo_mono.jpg", best_seller=True, rating=4.5, num_reviews=312),
        Product(name="Black Leather Chelsea Boots", description="Handcrafted leather Chelsea boots with elastic side panels and a stacked heel. Comfortable enough for all-day wear with a sleek profile that elevates any outfit. Exclusively from BloodFord Fashion Brand.", price=195000, original_price=240000, category="men", subcategory="shoes", image="boots_black.jpg", featured=True, rating=4.8, num_reviews=98),
        Product(name="Designer Black Joggers", description="Where comfort meets high fashion. These premium joggers feature a tapered fit, zippered pockets, and the subtle BloodFord Fashion Brand branding. Perfect for the modern gentleman on the move.", price=75000, category="men", subcategory="casual", image="joggers_black.jpg", new_arrival=True, rating=4.4, num_reviews=145),

        # ── Women's Collection ───────────────────────────────────────
        Product(name="Elegant Red Evening Gown", description="Absolutely stunning floor-length gown in vibrant red. Features a fitted bodice, flowing skirt, and delicate off-shoulder design. Turn heads at any gala or formal event. A BloodFord Fashion Brand masterpiece.", price=320000, original_price=400000, category="women", subcategory="dresses", image="gown_red.jpg", featured=True, best_seller=True, rating=4.9, num_reviews=87),
        Product(name="Black Power Pantsuit", description="Command any room in this impeccably tailored black pantsuit. Features a double-breasted blazer with gold-tone buttons and high-waisted wide-leg trousers. The epitome of feminine power dressing by BloodFord Fashion Brand.", price=265000, category="women", subcategory="suits", image="pantsuit_black.jpg", featured=True, new_arrival=True, rating=4.8, num_reviews=63),
        Product(name="White Silk Blouse", description="Luxurious white silk blouse with a relaxed fit and elegant draping. Features pearl buttons, a mandarin collar, and French cuffs. Versatile enough for both boardroom and brunch. BloodFord Fashion Brand original.", price=95000, category="women", subcategory="tops", image="blouse_white.jpg", best_seller=True, rating=4.7, num_reviews=178),
        Product(name="Red Pencil Skirt", description="Classic pencil skirt in bold red. Made from stretch fabric with a flattering high-waisted design and back slit. Pairs perfectly with our silk blouses for a complete BloodFord Fashion Brand look.", price=78000, original_price=90000, category="women", subcategory="skirts", image="skirt_red.jpg", featured=True, rating=4.6, num_reviews=134),
        Product(name="Black Leather Handbag", description="Structured leather handbag with gold hardware and signature BloodFord Fashion Brand lining. Features multiple compartments, a detachable shoulder strap, and protective metal feet. The ultimate accessory.", price=185000, original_price=225000, category="women", subcategory="accessories", image="bag_black.jpg", featured=True, best_seller=True, rating=4.9, num_reviews=256),
        Product(name="Monochrome Wrap Dress", description="Effortlessly elegant wrap dress in a black and white print. The flattering silhouette suits every body type with an adjustable waist tie and flowing midi length. A BloodFord Fashion Brand bestseller.", price=125000, category="women", subcategory="dresses", image="wrap_dress.jpg", best_seller=True, rating=4.7, num_reviews=198),
        Product(name="Red Stiletto Heels", description="Show-stopping red stiletto heels with a pointed toe and 4-inch heel. Made from premium materials with a cushioned insole for comfort. The perfect finishing touch to any BloodFord Fashion Brand outfit.", price=135000, category="women", subcategory="shoes", image="heels_red.jpg", new_arrival=True, rating=4.5, num_reviews=89),
        Product(name="Black Cropped Jacket", description="Chic cropped jacket in jet black with structured shoulders and a modern boxy silhouette. Features contrast stitching and branded buttons. Layer over dresses or casual wear for instant BloodFord Fashion Brand style.", price=155000, original_price=185000, category="women", subcategory="jackets", image="crop_jacket.jpg", new_arrival=True, featured=True, rating=4.6, num_reviews=72),

        # ── Unisex Collection ────────────────────────────────────────
        Product(name="Signature Logo Hoodie", description="Premium heavyweight hoodie featuring the iconic BloodFord Fashion Brand logo. Oversized fit with a kangaroo pocket, ribbed cuffs, and brushed fleece interior. Available in black, white, and red.", price=95000, category="unisex", subcategory="hoodies", image="hoodie_logo.jpg", featured=True, best_seller=True, new_arrival=True, rating=4.8, num_reviews=345),
        Product(name="Classic Logo T-Shirt", description="The essential BloodFord Fashion Brand tee. Made from 100% organic cotton with a relaxed fit and screen-printed logo. A wardrobe staple that represents the brand's commitment to quality and style.", price=45000, category="unisex", subcategory="tshirts", image="tshirt_logo.jpg", best_seller=True, rating=4.6, num_reviews=567),
        Product(name="Designer Sunglasses", description="Oversized aviator sunglasses with UV400 protection. Features lightweight metal frames and the BloodFord Fashion Brand insignia on the temple. Includes a branded leather case.", price=85000, category="unisex", subcategory="accessories", image="sunglasses.jpg", new_arrival=True, rating=4.5, num_reviews=123),
        Product(name="Premium Leather Belt", description="Handcrafted leather belt with a sleek matte-black buckle. Reversible design with black on one side and deep red on the other. A subtle yet powerful BloodFord Fashion Brand accessory.", price=55000, category="unisex", subcategory="accessories", image="belt_leather.jpg", best_seller=True, rating=4.7, num_reviews=234),
    ]

    for p in products:
        db.session.add(p)

    db.session.commit()
    print("✅ Database seeded with products!")


def initialize_database():
    with app.app_context():
        db.create_all()
        seed_products()


initialize_database()


# ══════════════════════════════════════════════════════════════════════
# RUN APP
# ══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
