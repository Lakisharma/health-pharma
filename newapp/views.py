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
    Order, OrderItem, ContactMessage
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


# ==================== User Profile & Dashboard ====================
@login_required(login_url='login')
def user_dashboard(request):
    """User dashboard"""
    user = request.user
    orders = user.orders.all()
    prescriptions = user.prescriptions.all()
    cart = user.cart
    
    context = {
        'orders': orders,
        'prescriptions': prescriptions,
        'cart': cart,
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
        
        cart = request.user.cart
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
    cart = request.user.cart
    
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
            
            # Move cart items to order
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.get_display_price(),
                )
            
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, f'Order {order.order_number} created successfully!')
            return redirect('order_confirmation', order_id=order.id)
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