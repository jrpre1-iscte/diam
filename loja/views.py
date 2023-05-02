from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ClothingItem, CartItem, Purchase
from .forms import CartItemForm


def index(request):
    items = ClothingItem.objects.filter(sold=False)
    context = {'items': items}
    return render(request, 'index.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sua conta foi criada com sucesso! Agora você pode fazer login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'register.html', context)


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(buyer=request.user)
    context = {'cart_items': cart_items}
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(ClothingItem, pk=item_id)
    form = CartItemForm(request.POST or None)
    if form.is_valid():
        quantity = form.cleaned_data.get('quantity')
        CartItem.objects.create(item=item, buyer=request.user, quantity=quantity)
        messages.success(request, 'Item adicionado ao carrinho.')
        return redirect('cart')
    context = {'item': item, 'form': form}
    return render(request, 'add_to_cart.html', context)


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id, buyer=request.user)
    if request.method == 'POST':
        cart_item.delete()
        messages.success(request, 'Item removido do carrinho.')
        return redirect('cart')
    context = {'cart_item': cart_item}
    return render(request, 'remove_from_cart.html', context)


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(buyer=request.user)
    for cart_item in cart_items:
        Purchase.objects.create(item=cart_item.item, buyer=request.user)
        cart_item.delete()
    messages.success(request, 'Sua compra foi finalizada. Obrigado!')
    return redirect('index')


@login_required
def purchase_history(request):
    purchases = Purchase.objects.filter(buyer=request.user)
    context = {'purchases': purchases}
    return render(request, 'purchase_history.html', context)
