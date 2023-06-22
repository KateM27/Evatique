from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .forms import AddToCartForm, RegistrationForm
from .models import Category, Product, Cart, Order


def home(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    products = Product.objects.all()
    categories = Category.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    return render(request, 'home.html', {
        'categories': categories,
        'products': products,
        'query': query,
        'category_id': int(category_id)
    })

def loginUser(request):
    # handle login request
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('home')
        else:
            messages.success(request, "Error logging in. Try again!")
            return redirect('home')
    else:
        return render(request, 'login.html', {})

def logoutUser(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

def registerUser(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Signed up successfully")
            return redirect('home')
    else:
        form = RegistrationForm()
        return render(request, 'signup.html', {'form':form})
    return render(request, 'signup.html', {'form':form})

def productDetail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[0:3]

    return render(request, 'productDetail.html', {
        'product': product,
        'related_products': related_products
    })

def addToCart(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart = request.session.get('cart', {})
            cart[product_id] = cart.get(product_id, 0) + quantity
            request.session['cart'] = cart
            
            return redirect('detail')
    else:
        form = AddToCartForm()

    return render(request, 'cart.html', {'form': form, 'product': product_id})


def cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total = sum(item.subtotal() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def placeOrder(request):
    if request.method == 'POST':
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        total = sum(item.subtotal() for item in cart_items)
        order = Order.objects.create(user=user, total=total)
        order.items.set(cart_items)
        order.calculate_total()
        order.save()
        # Clear the user's cart after placing the order
        cart_items.delete()
        return redirect('order_success')
    return redirect('cart')