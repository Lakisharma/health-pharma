from django import forms
from django.contrib.auth.models import User
from .models import Review, Prescription, Order, ContactMessage, Category, Product, CompanyInfo


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Stars') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your experience with this product...',
                'class': 'form-control'
            }),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['doctor_name', 'prescription_date', 'file', 'notes']
        widgets = {
            'prescription_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_name', 'shipping_phone', 'shipping_email', 'shipping_address', 
                  'shipping_city', 'shipping_state', 'shipping_zip', 'payment_method', 'notes']
        widgets = {
            'shipping_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'shipping_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'shipping_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'shipping_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Enter full delivery address'}),
            'shipping_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
            'shipping_state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter state'}),
            'shipping_zip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ZIP code'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Add any special delivery notes...'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


class ProductSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search products...',
        'class': 'form-control'
    }))
    category = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Filter by category...',
        'class': 'form-control'
    }))
    sort = forms.ChoiceField(required=False, choices=[
        ('newest', 'Newest'),
        ('price_low', 'Price: Low to High'),
        ('price_high', 'Price: High to Low'),
        ('rating', 'Top Rated'),
    ], widget=forms.Select(attrs={'class': 'form-control'}))


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'generic_name', 'category', 'description', 'price', 
            'discount_price', 'stock', 'unit', 'strength', 'manufacturer', 
            'expiry_date', 'requires_prescription', 'image', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'generic_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'strength': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'requires_prescription': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = ['company_name', 'phone', 'email', 'address', 'city', 'state', 'zip_code', 'about', 'logo']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class AdminOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'payment_status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'payment_status': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_staff', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
