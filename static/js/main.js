/* ════════════════════════════════════════════════════════════════════
   BLOODFORD FASHION BRAND — Main JavaScript
   ════════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

    // ── Navbar Scroll Effect ─────────────────────────────────────────
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // ── Hamburger Menu ───────────────────────────────────────────────
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });
    }

    // ── Search Toggle ────────────────────────────────────────────────
    const searchToggle = document.getElementById('searchToggle');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchClose = document.getElementById('searchClose');

    if (searchToggle && searchOverlay) {
        searchToggle.addEventListener('click', () => {
            searchOverlay.classList.toggle('active');
            if (searchOverlay.classList.contains('active')) {
                searchOverlay.querySelector('input').focus();
            }
        });

        if (searchClose) {
            searchClose.addEventListener('click', () => {
                searchOverlay.classList.remove('active');
            });
        }
    }

    // ── Flash Messages Auto-dismiss ──────────────────────────────────
    const flashContainer = document.getElementById('flashContainer');
    if (flashContainer) {
        setTimeout(() => {
            flashContainer.querySelectorAll('.flash-message').forEach((msg, i) => {
                setTimeout(() => {
                    msg.style.opacity = '0';
                    msg.style.transform = 'translateX(50px)';
                    setTimeout(() => msg.remove(), 300);
                }, i * 200);
            });
        }, 4000);
    }

    // ── Back to Top Button ───────────────────────────────────────────
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 500) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });

        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ── Newsletter Form ──────────────────────────────────────────────
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = newsletterForm.querySelector('input[type="email"]').value;

            try {
                const res = await fetch('/api/newsletter', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email })
                });
                const data = await res.json();
                showToast(data.message, data.success ? 'success' : 'error');
                if (data.success) newsletterForm.reset();
            } catch (err) {
                showToast('Something went wrong.', 'error');
            }
        });
    }

    // ── Countdown Timer ──────────────────────────────────────────────
    const countdownEl = document.getElementById('countdownTimer');
    if (countdownEl) {
        const targetDate = new Date(countdownEl.dataset.target).getTime();

        function updateCountdown() {
            const now = new Date().getTime();
            const distance = targetDate - now;

            if (distance <= 0) {
                countdownEl.innerHTML = '<p style="font-size: 1.2rem;">Package should have arrived!</p>';
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            document.getElementById('countDays').textContent = String(days).padStart(2, '0');
            document.getElementById('countHours').textContent = String(hours).padStart(2, '0');
            document.getElementById('countMinutes').textContent = String(minutes).padStart(2, '0');
            document.getElementById('countSeconds').textContent = String(seconds).padStart(2, '0');
        }

        updateCountdown();
        setInterval(updateCountdown, 1000);
    }
});


// ══════════════════════════════════════════════════════════════════════
// TOAST NOTIFICATIONS
// ══════════════════════════════════════════════════════════════════════

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = 'toast';

    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        info: 'fa-info-circle'
    };

    toast.innerHTML = `
        <i class="fas ${icons[type] || icons.info}"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(50px)';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}


// ══════════════════════════════════════════════════════════════════════
// CART FUNCTIONS
// ══════════════════════════════════════════════════════════════════════

async function addToCart(productId, size, color, quantity = 1) {
    try {
        const res = await fetch('/api/cart/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId, size, color, quantity })
        });

        if (res.status === 401) {
            showToast('Please log in to add items to cart.', 'error');
            setTimeout(() => window.location.href = '/login', 1500);
            return;
        }

        const data = await res.json();
        if (data.success) {
            showToast(data.message, 'success');
            updateCartBadge(data.cart_count);
        } else {
            showToast(data.message, 'error');
        }
    } catch (err) {
        showToast('Something went wrong.', 'error');
    }
}

async function removeFromCart(itemId) {
    try {
        const res = await fetch('/api/cart/remove', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ item_id: itemId })
        });
        const data = await res.json();
        if (data.success) {
            showToast('Item removed from cart.', 'info');
            updateCartBadge(data.cart_count);
            location.reload();
        }
    } catch (err) {
        showToast('Something went wrong.', 'error');
    }
}

async function updateCartItem(itemId, quantity) {
    try {
        const res = await fetch('/api/cart/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ item_id: itemId, quantity })
        });
        const data = await res.json();
        if (data.success) {
            document.getElementById('subtotal').textContent = formatPrice(data.subtotal);
            document.getElementById('shipping').textContent = formatPrice(data.shipping);
            document.getElementById('total').textContent = formatPrice(data.total);
            updateCartBadge(data.cart_count);
        }
    } catch (err) {
        showToast('Something went wrong.', 'error');
    }
}

function updateCartBadge(count) {
    let badge = document.getElementById('cartBadge');
    if (count > 0) {
        if (!badge) {
            const cartBtn = document.querySelector('.cart-btn');
            if (cartBtn) {
                badge = document.createElement('span');
                badge.className = 'cart-badge';
                badge.id = 'cartBadge';
                cartBtn.appendChild(badge);
            }
        }
        if (badge) badge.textContent = count;
    } else if (badge) {
        badge.remove();
    }
}

function formatPrice(amount) {
    return 'UGX ' + Number(amount).toLocaleString();
}


// ══════════════════════════════════════════════════════════════════════
// WISHLIST FUNCTIONS
// ══════════════════════════════════════════════════════════════════════

async function toggleWishlist(productId, btn) {
    try {
        const res = await fetch('/api/wishlist/toggle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId })
        });

        if (res.status === 401) {
            showToast('Please log in to use the wishlist.', 'error');
            setTimeout(() => window.location.href = '/login', 1500);
            return;
        }

        const data = await res.json();
        if (data.success) {
            showToast(data.message, 'success');
            if (btn) {
                btn.classList.toggle('wishlisted');
                const icon = btn.querySelector('i');
                if (data.action === 'added') {
                    icon.className = 'fas fa-heart';
                } else {
                    icon.className = 'far fa-heart';
                }
            }
        }
    } catch (err) {
        showToast('Something went wrong.', 'error');
    }
}


// ══════════════════════════════════════════════════════════════════════
// PRODUCT DETAIL PAGE
// ══════════════════════════════════════════════════════════════════════

function selectSize(btn) {
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
}

function selectColor(btn) {
    document.querySelectorAll('.color-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
}

function changeQuantity(change) {
    const input = document.getElementById('quantityInput');
    let val = parseInt(input.value) + change;
    if (val < 1) val = 1;
    if (val > 99) val = 99;
    input.value = val;
}


// ══════════════════════════════════════════════════════════════════════
// CHECKOUT & PAYMENT SIMULATION
// ══════════════════════════════════════════════════════════════════════

function selectPayment(method) {
    document.querySelectorAll('.payment-method').forEach(m => m.classList.remove('selected'));
    document.querySelector(`[data-method="${method}"]`).classList.add('selected');

    document.querySelectorAll('.payment-details').forEach(d => d.classList.remove('active'));
    const details = document.getElementById(`${method}-details`);
    if (details) details.classList.add('active');
}

async function processCheckout() {
    // Gather form data
    const address = document.getElementById('shippingAddress')?.value;
    const city = document.getElementById('shippingCity')?.value;
    const country = document.getElementById('shippingCountry')?.value;
    const notes = document.getElementById('orderNotes')?.value;

    const selectedPayment = document.querySelector('.payment-method.selected');
    if (!selectedPayment) {
        showToast('Please select a payment method.', 'error');
        return;
    }

    if (!address || !city || !country) {
        showToast('Please fill in all shipping details.', 'error');
        return;
    }

    const paymentMethod = selectedPayment.dataset.method;

    // Show payment simulation modal
    const modal = document.getElementById('paymentModal');
    modal.classList.add('active');

    const formSection = document.getElementById('paymentFormSection');
    const processingSection = document.getElementById('paymentProcessing');
    const successSection = document.getElementById('paymentSuccess');

    formSection.style.display = 'block';
    processingSection.style.display = 'none';
    successSection.style.display = 'none';

    // Update modal based on payment method
    const modalTitle = modal.querySelector('.modal-header h2');
    if (paymentMethod === 'mobile_money') {
        modalTitle.textContent = '📱 Mobile Money Payment';
        formSection.innerHTML = `
            <div class="form-group">
                <label>Mobile Money Number</label>
                <input type="tel" class="form-control" id="momoNumber" placeholder="e.g. 0770 123 456" value="0770 000 000">
            </div>
            <div class="form-group">
                <label>Network</label>
                <select class="form-control" id="momoNetwork">
                    <option value="mtn">MTN Mobile Money</option>
                    <option value="airtel">Airtel Money</option>
                </select>
            </div>
            <p style="color: var(--gray-600); font-size: 0.85rem; margin-top: 10px;">
                <i class="fas fa-lock" style="color: var(--red);"></i> 
                A prompt will be sent to your phone. Enter your PIN to confirm.
            </p>
        `;
    } else if (paymentMethod === 'visa') {
        modalTitle.textContent = '💳 Visa Card Payment';
        formSection.innerHTML = `
            <div class="form-group">
                <label>Card Number</label>
                <input type="text" class="form-control" placeholder="4242 4242 4242 4242" value="4242 4242 4242 4242" maxlength="19">
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Expiry Date</label>
                    <input type="text" class="form-control" placeholder="MM/YY" value="12/28">
                </div>
                <div class="form-group">
                    <label>CVV</label>
                    <input type="text" class="form-control" placeholder="123" value="123" maxlength="3">
                </div>
            </div>
            <div class="form-group">
                <label>Cardholder Name</label>
                <input type="text" class="form-control" placeholder="John Doe" value="John Doe">
            </div>
            <p style="color: var(--gray-600); font-size: 0.85rem; margin-top: 10px;">
                <i class="fas fa-shield-alt" style="color: var(--red);"></i> 
                Your card information is securely encrypted.
            </p>
        `;
    } else {
        modalTitle.textContent = '💳 Mastercard Payment';
        formSection.innerHTML = `
            <div class="form-group">
                <label>Card Number</label>
                <input type="text" class="form-control" placeholder="5500 0000 0000 0004" value="5500 0000 0000 0004" maxlength="19">
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Expiry Date</label>
                    <input type="text" class="form-control" placeholder="MM/YY" value="12/28">
                </div>
                <div class="form-group">
                    <label>CVV</label>
                    <input type="text" class="form-control" placeholder="123" value="123" maxlength="3">
                </div>
            </div>
            <div class="form-group">
                <label>Cardholder Name</label>
                <input type="text" class="form-control" placeholder="John Doe" value="John Doe">
            </div>
            <p style="color: var(--gray-600); font-size: 0.85rem; margin-top: 10px;">
                <i class="fas fa-shield-alt" style="color: var(--red);"></i> 
                Your card information is securely encrypted.
            </p>
        `;
    }

    // Store payment data for later
    window._checkoutData = { address, city, country, notes, payment_method: paymentMethod };
}

async function confirmPayment() {
    const modal = document.getElementById('paymentModal');
    const formSection = document.getElementById('paymentFormSection');
    const processingSection = document.getElementById('paymentProcessing');
    const successSection = document.getElementById('paymentSuccess');
    const confirmBtn = document.getElementById('confirmPayBtn');
    const cancelBtn = document.getElementById('cancelPayBtn');

    // Show processing
    formSection.style.display = 'none';
    processingSection.style.display = 'block';
    confirmBtn.style.display = 'none';
    cancelBtn.style.display = 'none';

    // Simulate payment processing delay
    await new Promise(resolve => setTimeout(resolve, 3000));

    try {
        const res = await fetch('/api/place-order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(window._checkoutData)
        });

        const data = await res.json();

        processingSection.style.display = 'none';

        if (data.success) {
            successSection.style.display = 'block';
            successSection.innerHTML = `
                <div style="text-align: center; padding: 30px 0;">
                    <div style="width: 70px; height: 70px; background: #E8F5E9; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 2rem; color: #4CAF50;">
                        <i class="fas fa-check"></i>
                    </div>
                    <h3 style="font-family: var(--font-display); margin-bottom: 8px;">Payment Successful!</h3>
                    <p style="color: var(--gray-600); margin-bottom: 8px;">Order Number: <strong style="color: var(--red);">${data.order_number}</strong></p>
                    <p style="color: var(--gray-600); font-size: 0.9rem;">You will be redirected to your order confirmation...</p>
                </div>
            `;

            setTimeout(() => {
                window.location.href = `/payment-success/${data.order_number}`;
            }, 2500);
        } else {
            showToast(data.message || 'Order failed.', 'error');
            modal.classList.remove('active');
        }
    } catch (err) {
        showToast('Something went wrong. Please try again.', 'error');
        modal.classList.remove('active');
    }
}

function closePaymentModal() {
    document.getElementById('paymentModal').classList.remove('active');
}


// ══════════════════════════════════════════════════════════════════════
// REVIEW SYSTEM
// ══════════════════════════════════════════════════════════════════════

let selectedRating = 5;

function setRating(rating) {
    selectedRating = rating;
    document.querySelectorAll('.review-star').forEach((star, i) => {
        star.classList.toggle('active', i < rating);
    });
}

async function submitReview(productId) {
    const comment = document.getElementById('reviewComment')?.value || '';

    try {
        const res = await fetch('/api/review', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId, rating: selectedRating, comment })
        });

        const data = await res.json();
        showToast(data.message, data.success ? 'success' : 'error');
        if (data.success) {
            setTimeout(() => location.reload(), 1500);
        }
    } catch (err) {
        showToast('Something went wrong.', 'error');
    }
}


// ══════════════════════════════════════════════════════════════════════
// SHOP PAGE — SORT & FILTER
// ══════════════════════════════════════════════════════════════════════

function applySorting(sortValue) {
    const url = new URL(window.location);
    url.searchParams.set('sort', sortValue);
    window.location.href = url.toString();
}

function applyFilter(key, value) {
    const url = new URL(window.location);
    url.searchParams.set(key, value);
    url.searchParams.delete('page');
    window.location.href = url.toString();
}

function removeFilter(key) {
    const url = new URL(window.location);
    url.searchParams.delete(key);
    window.location.href = url.toString();
}
