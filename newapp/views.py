from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from datetime import datetime
from .models import (
    CompanyInfo, Category, Product, Review, Prescription, Cart, CartItem, 
    Order, OrderItem, ContactMessage, Notification
)
from .forms import (
    UserRegisterForm, UserLoginForm, UserProfileForm, ReviewForm, 
    PrescriptionForm, OrderForm, ContactForm, ProductSearchForm
)


# ==================== Home Page ====================
def home(request):
    """Home page with featured products"""
    featured_products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()
    company = CompanyInfo.objects.first()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'company': company,
    }
    return render(request, 'home.html', context)


# ==================== Product Listing & Search ====================
def product_list(request):
    """Product listing page with filtering and search"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    form = ProductSearchForm(request.GET)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(generic_name__icontains=search_query)
        )
    
    # Category Filter
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category__name__icontains=category_filter)
    
    # Sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')
    
    context = {
        'products': products,
        'categories': categories,
        'form': form,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request, 'products.html', context)


# ==================== Product Detail ====================
def product_detail(request, product_id):
    """Product detail page with reviews"""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product_id)[:4]
    
    review_form = None
    if request.user.is_authenticated:
        review_form = ReviewForm()
        if request.method == 'POST' and 'submit_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review, created = Review.objects.update_or_create(
                    product=product,
                    user=request.user,
                    defaults={
                        'rating': review_form.cleaned_data['rating'],
                        'comment': review_form.cleaned_data['comment'],
                    }
                )
                messages.success(request, 'Your review has been submitted!')
                return redirect('product_detail', product_id=product_id)
    
    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'review_form': review_form,
    }
    return render(request, 'product_detail.html', context)


# ==================== User Authentication ====================
def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            # Create cart for new user
            Cart.objects.create(user=user)
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})


def user_login(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


@login_required(login_url='login')
def user_dashboard(request):
    """User dashboard"""
    user = request.user
    orders = user.orders.all()
    prescriptions = user.prescriptions.all()
    try:
        cart = user.cart
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
    
    # Calculate dynamic total spent (excluding cancelled orders)
    from django.db.models import Sum
    total_spent_query = orders.exclude(status='cancelled').aggregate(Sum('total_amount'))['total_amount__sum']
    total_spent = total_spent_query if total_spent_query is not None else 0
    
    context = {
        'orders': orders,
        'prescriptions': prescriptions,
        'cart': cart,
        'total_spent': total_spent,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def user_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})


# ==================== Shopping Cart ====================
@login_required(login_url='login')
def view_cart(request):
    """View shopping cart"""
    try:
        cart = request.user.cart
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    
    context = {'cart': cart}
    return render(request, 'cart.html', context)


@login_required(login_url='login')
@require_POST
def add_to_cart(request):
    """Add product to cart (AJAX)"""
    try:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id)
        
        if product.stock < quantity:
            return JsonResponse({'status': 'error', 'message': 'Insufficient stock'}, status=400)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'{product.name} added to cart!',
            'cart_count': cart.get_item_count(),
            'cart_total': str(cart.get_total())
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    try:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
        else:
            if cart_item.product.stock < quantity:
                return JsonResponse({'status': 'error', 'message': 'Insufficient stock'}, status=400)
            cart_item.quantity = quantity
            cart_item.save()
        
        try:
            cart = request.user.cart
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
        return JsonResponse({
            'status': 'success',
            'cart_total': str(cart.get_total()),
            'item_total': str(cart_item.get_total() if quantity > 0 else 0)
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('view_cart')


# ==================== Checkout & Orders ====================
@login_required(login_url='login')
def checkout(request):
    """Checkout page"""
    try:
        cart = request.user.cart
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('view_cart')
    
    # Check for prescription requirements
    prescription_required = cart.items.filter(product__requires_prescription=True).exists()
    user_prescriptions = request.user.prescriptions.filter(verified=True)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Check prescription if required
            if prescription_required:
                prescription_id = request.POST.get('prescription')
                if not prescription_id:
                    messages.error(request, 'Prescription required for some items!')
                    context = {
                        'form': form,
                        'cart': cart,
                        'prescription_required': prescription_required,
                        'user_prescriptions': user_prescriptions,
                    }
                    return render(request, 'checkout.html', context)
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=cart.get_total(),
                shipping_name=form.cleaned_data['shipping_name'],
                shipping_phone=form.cleaned_data['shipping_phone'],
                shipping_email=form.cleaned_data['shipping_email'],
                shipping_address=form.cleaned_data['shipping_address'],
                shipping_city=form.cleaned_data['shipping_city'],
                shipping_state=form.cleaned_data['shipping_state'],
                shipping_zip=form.cleaned_data['shipping_zip'],
                payment_method=form.cleaned_data['payment_method'],
                notes=form.cleaned_data['notes'],
                prescription_required=prescription_required,
            )
            
            if prescription_required and request.POST.get('prescription'):
                order.prescription_id = request.POST.get('prescription')
                order.save()
            
            # Move cart items to order and deduct stock
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.get_display_price(),
                )
                
                # Dynamic inventory level adjustment
                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()
            
            # Clear cart
            cart.items.all().delete()
            
            # Create admin notification
            Notification.objects.create(
                title="New Order Received",
                message=f"Order {order.order_number} has been placed by {order.shipping_name} for ₹{order.total_amount}.",
                order=order,
                is_admin=True
            )
            
            messages.success(request, f'Order {order.order_number} created successfully!')
            return redirect('order_confirmation', order_id=order.id)
        else:
            # Extract and display specific validation errors in toast messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = OrderForm(initial={
            'shipping_name': request.user.get_full_name() or request.user.username,
            'shipping_email': request.user.email,
        })
    
    context = {
        'form': form,
        'cart': cart,
        'prescription_required': prescription_required,
        'user_prescriptions': user_prescriptions,
    }
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'order_confirmation.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    """Order detail page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'order_detail.html', context)


@login_required(login_url='login')
def order_invoice(request, order_id):
    """Invoice view styled for printing/saving as PDF"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    company = CompanyInfo.objects.first()
    context = {
        'order': order,
        'company': company,
    }
    return render(request, 'order_invoice.html', context)


# ==================== Prescriptions ====================
@login_required(login_url='login')
def my_prescriptions(request):
    """User prescriptions"""
    prescriptions = request.user.prescriptions.all()
    context = {'prescriptions': prescriptions}
    return render(request, 'prescriptions.html', context)


@login_required(login_url='login')
def upload_prescription(request):
    """Upload prescription"""
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.user = request.user
            prescription.save()
            messages.success(request, 'Prescription uploaded successfully! Admin will verify it.')
            return redirect('my_prescriptions')
    else:
        form = PrescriptionForm()
    
    return render(request, 'upload_prescription.html', {'form': form})


# ==================== Contact ====================
def contact(request):
    """Contact form"""
    company = CompanyInfo.objects.first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! We will contact you soon.')
            return redirect('home')
    else:
        form = ContactForm()
        if request.user.is_authenticated:
            form.fields['name'].initial = request.user.get_full_name() or request.user.username
            form.fields['email'].initial = request.user.email
    
    context = {'form': form, 'company': company}
    return render(request, 'contact.html', context)


# ==================== About ====================
def about(request):
    """About page"""
    company = CompanyInfo.objects.first()
    context = {'company': company}
    return render(request, 'about.html', context)


# ==================== Forgot Password ====================
import random
from django.core.mail import send_mail
from datetime import timedelta

def forgot_password(request):
    """Forgot password page - sends 6-digit OTP to user's email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        users = User.objects.filter(email=email)
        
        if not users.exists():
            messages.error(request, 'No registered user found with this email address.')
            return render(request, 'forgot_password.html')
            
        user = users.first()
        
        # Generate 6-digit OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Store in session with 5 minutes expiry
        request.session['reset_user_id'] = str(user.id)
        request.session['reset_otp'] = otp
        request.session['reset_otp_expiry'] = (datetime.now() + timedelta(minutes=5)).timestamp()
        request.session['otp_verified'] = False
        
        # Send OTP email
        try:
            subject = 'Password Reset OTP - Healeaf Pharma'
            message = f'Hello {user.username},\n\nYour One-Time Password (OTP) to reset your Healeaf Pharma account password is: {otp}\n\nThis OTP is valid for 5 minutes only.\n\nIf you did not request this password reset, please ignore this email.'
            from_email = 'support@healeafpharma.com'
            recipient_list = [email]
            
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'A 6-digit OTP verification code has been sent to your email address!')
            return redirect('verify_otp')
        except Exception as e:
            messages.error(request, f'Failed to send email: {str(e)}')
            return render(request, 'forgot_password.html')
            
    return render(request, 'forgot_password.html')


def verify_otp(request):
    """Verify OTP verification code entered by user"""
    if 'reset_otp' not in request.session or 'reset_user_id' not in request.session:
        messages.warning(request, 'Session expired or invalid. Please start again.')
        return redirect('forgot_password')
        
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('reset_otp')
        expiry = request.session.get('reset_otp_expiry', 0)
        
        if datetime.now().timestamp() > expiry:
            messages.error(request, 'The OTP has expired. Please request a new one.')
            return redirect('forgot_password')
            
        if user_otp == session_otp:
            request.session['otp_verified'] = True
            messages.success(request, 'OTP verified successfully! Please choose a new password.')
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP code. Please check and try again.')
            
    return render(request, 'verify_otp.html')


def reset_password(request):
    """Reset user password after OTP verification"""
    if not request.session.get('otp_verified') or 'reset_user_id' not in request.session:
        messages.error(request, 'Unauthorized password reset attempt.')
        return redirect('forgot_password')
        
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'reset_password.html')
            
        try:
            user_id = request.session.get('reset_user_id')
            user = User.objects.get(id=user_id)
            user.set_password(password)
            user.save()
            
            # Clear reset session keys
            keys_to_delete = ['reset_user_id', 'reset_otp', 'reset_otp_expiry', 'otp_verified']
            for key in keys_to_delete:
                if key in request.session:
                    del request.session[key]
                    
            messages.success(request, 'Your password has been successfully reset! Please login with your new password.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            
    return render(request, 'reset_password.html')


# ==================== Admin Panel ====================
from .forms import CategoryForm, ProductForm, CompanyInfoForm, AdminOrderForm, AdminUserForm

def admin_login(request):
    """Admin login"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, 'Admin login successful!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions!')
    
    return render(request, 'admin/login.html')


def admin_logout(request):
    """Admin logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('admin_login')


def admin_dashboard(request):
    """Admin dashboard with stats and graphs"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    # Statistics
    from django.db.models import Sum
    revenue_sum = Order.objects.exclude(status='cancelled').aggregate(Sum('total_amount'))['total_amount__sum']
    total_revenue = revenue_sum if revenue_sum is not None else 0.0
    
    total_orders = Order.objects.count()
    total_users = User.objects.exclude(username='admin').count()
    total_products = Product.objects.count()
    pending_prescriptions = Prescription.objects.filter(is_verified=False).count()
    total_messages = ContactMessage.objects.count()
    
    # Order statistics
    order_stats = {
        'pending': Order.objects.filter(status='pending').count(),
        'processing': Order.objects.filter(status__in=['confirmed', 'processing', 'shipped']).count(),
        'delivered': Order.objects.filter(status='delivered').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }
    
    # Recent orders and low stock
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    low_stock_products = Product.objects.filter(stock__lt=15).order_by('stock')[:5]
    
    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_products': total_products,
        'pending_prescriptions': pending_prescriptions,
        'total_messages': total_messages,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'order_stats': order_stats,
    }
    return render(request, 'admin/dashboard.html', context)


# --- Category Management CRUD ---
def admin_categories(request):
    """Admin category list"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    categories = Category.objects.all().order_by('name')
    return render(request, 'admin/categories.html', {'categories': categories})


def admin_category_add(request):
    """Add a category"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('admin_categories')
    else:
        form = CategoryForm()
    
    return render(request, 'admin/category_form.html', {'form': form})


def admin_category_edit(request, category_id):
    """Edit a category"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'admin/category_form.html', {'form': form})


def admin_category_delete(request, category_id):
    """Delete a category"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        messages.success(request, 'Category deleted successfully!')
    
    return redirect('admin_categories')


# --- Product Management CRUD ---
def admin_products(request):
    """Admin product list with search and filters"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('name')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(generic_name__icontains=search_query) |
            Q(manufacturer__icontains=search_query)
        )
    
    # Category Filter
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category__name=category_filter)
    
    # Stock Status Filter
    stock_status_filter = request.GET.get('stock_status', '')
    if stock_status_filter == 'low':
        products = products.filter(stock__lt=15, stock__gt=0)
    elif stock_status_filter == 'out':
        products = products.filter(stock=0)
        
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'stock_status_filter': stock_status_filter,
    }
    return render(request, 'admin/products.html', context)


def admin_product_add(request):
    """Add a product"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('admin_products')
    else:
        form = ProductForm()
    
    return render(request, 'admin/product_form.html', {'form': form})


def admin_product_edit(request, product_id):
    """Edit a product"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'admin/product_form.html', {'form': form})


def admin_product_delete(request, product_id):
    """Delete a product"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        messages.success(request, 'Product deleted successfully!')
    
    return redirect('admin_products')


# --- Order Management ---
def admin_orders(request):
    """Admin order tracker"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin/orders.html', {'orders': orders})


def admin_order_detail(request, order_id):
    """Order detail & invoice workspace"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/order_detail.html', {'order': order})


def admin_order_edit(request, order_id):
    """Edit order fulfillment status"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        form = AdminOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order details updated successfully!')
            return redirect('admin_order_detail', order_id=order.id)
        else:
            messages.error(request, 'Failed to update order details. Please verify fields.')
            return redirect('admin_order_detail', order_id=order.id)
            
    return redirect('admin_orders')


def admin_order_delete(request, order_id):
    """Delete order record"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        messages.success(request, 'Order record deleted successfully!')
        
    return redirect('admin_orders')


# --- Prescription Verification ---
def admin_prescriptions(request):
    """Admin prescription list"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    filter_status = request.GET.get('status', '')
    if filter_status == 'pending':
        prescriptions = Prescription.objects.filter(is_verified=False)
    elif filter_status == 'approved':
        prescriptions = Prescription.objects.filter(is_verified=True)
    else:
        prescriptions = Prescription.objects.all()
        
    prescriptions = prescriptions.order_by('-uploaded_at')
    
    context = {
        'prescriptions': prescriptions,
        'filter_status': filter_status,
    }
    return render(request, 'admin/prescriptions.html', context)


def admin_prescription_detail(request, prescription_id):
    """Prescription review screen"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    prescription = get_object_or_404(Prescription, id=prescription_id)
    return render(request, 'admin/prescription_detail.html', {'prescription': prescription})


def admin_approve_prescription(request, prescription_id):
    """Verify or reject prescription"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    prescription = get_object_or_404(Prescription, id=prescription_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('notes', '')
        
        if action == 'approve':
            prescription.is_verified = True
            prescription.verified = True
            prescription.verified_by = request.user
            prescription.notes = notes
            prescription.verified_at = datetime.now()
            prescription.save()
            messages.success(request, 'Prescription approved & verified successfully!')
            return redirect('admin_prescription_detail', prescription_id=prescription.id)
        elif action == 'reject':
            prescription.delete()
            messages.success(request, 'Prescription has been rejected & removed!')
            return redirect('admin_prescriptions')
            
    return redirect('admin_prescriptions')


# --- User Directory Management ---
def admin_users(request):
    """Admin user directory"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    users = User.objects.exclude(username='admin').order_by('-date_joined')
    return render(request, 'admin/users.html', {'users': users})


def admin_user_edit(request, user_id):
    """Edit user details and roles"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User permissions updated successfully!')
            return redirect('admin_users')
    else:
        form = AdminUserForm(instance=user)
        
    return render(request, 'admin/user_form.html', {'form': form})


def admin_user_toggle_status(request, user_id):
    """Quick toggle active / blocked status"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()
        status_str = 'activated' if user.is_active else 'suspended'
        messages.success(request, f'Account for {user.username} has been {status_str}!')
        
    return redirect('admin_users')


# --- Reviews Moderation ---
def admin_reviews(request):
    """List all user reviews"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'admin/reviews.html', {'reviews': reviews})


def admin_review_delete(request, review_id):
    """Delete review"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        messages.success(request, 'Customer review deleted successfully!')
        
    return redirect('admin_reviews')


# --- Contact Messages Inbox ---
def admin_messages(request):
    """Inbox for customer contact queries"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'admin/messages.html', {'messages_list': messages_list})


def admin_message_delete(request, message_id):
    """Delete customer message"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    if request.method == 'POST':
        msg = get_object_or_404(ContactMessage, id=message_id)
        msg.delete()
        messages.success(request, 'Contact message deleted successfully!')
        
    return redirect('admin_messages')


# --- Company Settings ---
def admin_company_settings(request):
    """Edit Company Details"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    company = CompanyInfo.objects.first()
    if not company:
        # Create empty base company config if none exists
        company = CompanyInfo.objects.create(company_name="Healeaf Pharma", email="support@healeafpharma.com")
        
    if request.method == 'POST':
        form = CompanyInfoForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company configurations updated successfully!')
            return redirect('admin_company_settings')
    else:
        form = CompanyInfoForm(instance=company)
        
    return render(request, 'admin/company_settings.html', {'form': form})


@login_required(login_url='login')
def admin_mark_notifications_read(request):
    """Mark all admin notifications as read"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    Notification.objects.filter(is_admin=True, is_read=False).update(is_read=True)
    messages.success(request, 'All notifications marked as read!')
    return redirect(request.META.get('HTTP_REFERER', 'admin_dashboard'))


from django.db import connection
from django.core.management import call_command
from io import StringIO

def debug_db(request):
    """Debug route to inspect SQLite database tables, run migrations, and seed data on Render"""
    result = {}
    
    # 1. Get database engine and path
    from django.conf import settings
    db_config = settings.DATABASES['default']
    result['engine'] = db_config['ENGINE']
    result['name'] = str(db_config['NAME'])
    
    # 2. Get list of existing tables
    try:
        tables = connection.introspection.table_names()
        result['tables'] = tables
        result['tables_count'] = len(tables)
    except Exception as e:
        result['tables_error'] = str(e)
        
    # 3. If query parameter 'action' is 'initialize'
    action = request.GET.get('action')
    if action == 'initialize':
        migrate_out = StringIO()
        setup_out = StringIO()
        try:
            call_command('migrate', stdout=migrate_out, stderr=migrate_out, interactive=False)
            result['migrate_status'] = 'success'
            result['migrate_output'] = migrate_out.getvalue()
        except Exception as e:
            result['migrate_status'] = 'failed'
            result['migrate_error'] = str(e)
            result['migrate_output'] = migrate_out.getvalue()
            
        try:
            call_command('setup', stdout=setup_out, stderr=setup_out, interactive=False)
            result['setup_status'] = 'success'
            result['setup_output'] = setup_out.getvalue()
        except Exception as e:
            result['setup_status'] = 'failed'
            result['setup_error'] = str(e)
            result['setup_output'] = setup_out.getvalue()
            
        # Re-fetch tables after initialization
        try:
            tables = connection.introspection.table_names()
            result['tables_after'] = tables
            result['tables_count_after'] = len(tables)
        except Exception as e:
            result['tables_after_error'] = str(e)
            
    return JsonResponse(result, json_dumps_params={'indent': 2})