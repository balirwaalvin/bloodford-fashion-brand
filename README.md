# BloodFord Fashion Brand 🛍️

![BloodFord Fashion Brand](https://raw.githubusercontent.com/balirwaalvin/bloodford-fashion-brand/main/static/images/preview.png)

A premium e-commerce fashion website featuring original designs for modern men and women. Built with Flask and modern web technologies.

## ✨ Features

- **User Authentication** - Secure login and registration system with Flask-Login
- **Product Catalog** - Browse men's, women's, and unisex collections
- **Shopping Cart** - Add products, manage quantities, select sizes and colors
- **Wishlist** - Save favorite items for later
- **Order Management** - Track orders with real-time status updates
- **User Profiles** - Manage personal information and view order history
- **Product Reviews** - Rate and review purchased products
- **Responsive Design** - Fully optimized for mobile, tablet, and desktop
- **Search & Filter** - Find products by category, price, and more
- **Admin Dashboard** - Manage products, orders, and users (admin access)

## 🎨 Brand Colors

- **Red:** `#C41E3A` - Bold and commanding
- **Black:** `#0A0A0A` - Elegant and timeless
- **White:** `#FFFFFF` - Clean and sophisticated

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/balirwaalvin/bloodford-fashion-brand.git
cd bloodford-fashion-brand
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## 📦 Dependencies

- **Flask 3.0.0** - Web framework
- **Flask-SQLAlchemy 3.1.1** - Database ORM
- **Flask-Login 0.6.3** - User session management
- **Flask-WTF 1.2.1** - Form handling and validation
- **Flask-Mail 0.9.1** - Email support
- **Werkzeug 3.0.1** - WSGI utilities
- **Pillow** - Image processing
- **email-validator** - Email validation

## 📂 Project Structure

```
bloodford-fashion-brand/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── instance/             # Database files (git-ignored)
├── static/               # Static assets
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   ├── js/
│   │   └── main.js      # JavaScript functionality
│   └── images/          # Logo and images
└── templates/            # HTML templates
    ├── base.html        # Base template
    ├── home.html        # Landing page
    ├── shop.html        # Product catalog
    ├── product_detail.html
    ├── cart.html        # Shopping cart
    ├── checkout.html    # Checkout process
    ├── orders.html      # Order history
    ├── profile.html     # User profile
    ├── wishlist.html    # Saved items
    ├── login.html       # Login page
    ├── register.html    # Registration
    ├── about.html       # About us
    ├── contact.html     # Contact form
    └── tracking.html    # Order tracking
```

## 🛠️ Technology Stack

- **Backend:** Flask (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML5, CSS3, JavaScript
- **Fonts:** Playfair Display, Inter, Bebas Neue
- **Icons:** Font Awesome 6.5.0

## 🔐 Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Secure session management
- SQL injection prevention via SQLAlchemy ORM

## 📱 Responsive Design

The website is fully responsive and tested on:
- Desktop (1920px+)
- Laptop (1366px - 1920px)
- Tablet (768px - 1366px)
- Mobile (320px - 768px)

## 🎯 Future Enhancements

- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Email notifications for orders
- [ ] Advanced product filtering
- [ ] Customer reviews and ratings
- [ ] Inventory management system
- [ ] Multi-language support
- [ ] Live chat support
- [ ] Social media integration

## 👨‍💻 Author

**Balirwa Alvin**
- Email: sanyukalvin@gmail.com
- GitHub: [@balirwaalvin](https://github.com/balirwaalvin)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Original design concept inspired by modern luxury fashion brands
- Icons provided by Font Awesome
- Fonts from Google Fonts

---

**BloodFord Fashion Brand** - *Redefining fashion for the modern individual* 🌟
