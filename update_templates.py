import os

replacements = {
    'templates/home.html': [
        ('<i class="fas fa-tshirt product-placeholder"></i>', '<img src="{{ url_for(\'static\', filename=\'images/\' ~ product.image) }}" alt="{{ product.name }}">')
    ],
    'templates/shop.html': [
        ('<i class="fas fa-tshirt product-placeholder"></i>', '<img src="{{ url_for(\'static\', filename=\'images/\' ~ product.image) }}" alt="{{ product.name }}">')
    ],
    'templates/product_detail.html': [
        # The main image for 'product'
        ('<div class="product-main-image">\n                    <i class="fas fa-tshirt product-placeholder"></i>', '<div class="product-main-image">\n                    <img src="{{ url_for(\'static\', filename=\'images/\' ~ product.image) }}" alt="{{ product.name }}" id="mainImage">'),
        # Thumbnails (just duplicate the main image for now or placeholders)
        ('<div class="thumb active"><i class="fas fa-tshirt"></i></div>', '<div class="thumb active"><img src="{{ url_for(\'static\', filename=\'images/\' ~ product.image) }}" alt="Thumb"></div>'),
        ('<div class="thumb"><i class="fas fa-tshirt"></i></div>', '<div class="thumb"><img src="{{ url_for(\'static\', filename=\'images/\' ~ product.image) }}" alt="Thumb"></div>'),
        # Related products loop (also uses "product" variable)
        ('<i class="fas fa-tshirt product-placeholder"></i>', '<img src="{{ url_for(\'static\', filename=\'images/\' ~ product.image) }}" alt="{{ product.name }}">')
    ],
    'templates/cart.html': [
        ('<i class="fas fa-tshirt"></i>', '<img src="{{ url_for(\'static\', filename=\'images/\' ~ item.product.image) }}" alt="{{ item.product.name }}">')
    ],
    'templates/checkout.html': [
        ('<i class="fas fa-tshirt"></i>', '<img src="{{ url_for(\'static\', filename=\'images/\' ~ item.product.image) }}" alt="{{ item.product.name }}">')
    ],
    'templates/orders.html': [
        ('<i class="fas fa-tshirt"></i>', '<img src="{{ url_for(\'static\', filename=\'images/\' ~ item.product.image) }}" alt="{{ item.product.name }}" style="width: 100%; height: 100%; object-fit: cover; border-radius: inherit;">')
    ],
    'templates/tracking.html': [
        ('<i class="fas fa-tshirt"></i>', '<img src="{{ url_for(\'static\', filename=\'images/\' ~ item.product.image) }}" alt="{{ item.product.name }}" style="width: 100%; height: 100%; object-fit: cover; border-radius: inherit;">')
    ],
    'templates/wishlist.html': [
        ('<i class="fas fa-tshirt product-placeholder"></i>', '<img src="{{ url_for(\'static\', filename=\'images/\' ~ item.product.image) }}" alt="{{ item.product.name }}">')
    ]
}

for filepath, repls in replacements.items():
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in repls:
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Update style.css
css_addition = """

/* Additional Image Styling */
.product-card-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}
.product-card:hover .product-card-image img {
    transform: scale(1.05);
}
.product-main-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.product-thumbnails .thumb {
    overflow: hidden;
    padding: 0; /* Remove padding to let image fill */
}
.product-thumbnails .thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.cart-item-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.summary-item-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: inherit;
}
"""

with open('static/css/style.css', 'a') as f:
    f.write(css_addition)

print("Done updating templates and CSS!")
