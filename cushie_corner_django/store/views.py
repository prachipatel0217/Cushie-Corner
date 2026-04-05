from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
import json

from .models import Product, CartItem, Order, OrderItem, ContactMessage


def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def index(request):
    products = Product.objects.filter(stock__gt=0)
    session_key = get_session_key(request)
    cart_count = CartItem.objects.filter(session_key=session_key).count()
    return render(request, 'store/index.html', {
        'products': products,
        'cart_count': cart_count,
    })


def cart(request):
    session_key = get_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key).select_related('product')
    total = sum(item.subtotal() for item in cart_items)
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_items.count(),
    })


@require_POST
def add_to_cart(request):
    session_key = get_session_key(request)
    data = json.loads(request.body)
    product_id = data.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        session_key=session_key,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart_count = CartItem.objects.filter(session_key=session_key).count()
    return JsonResponse({'success': True, 'cart_count': cart_count, 'message': f'{product.name} added to cart!'})


@require_POST
def remove_from_cart(request):
    session_key = get_session_key(request)
    data = json.loads(request.body)
    item_id = data.get('item_id')
    CartItem.objects.filter(id=item_id, session_key=session_key).delete()
    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.subtotal() for item in cart_items)
    return JsonResponse({'success': True, 'total': str(total), 'cart_count': cart_items.count()})


@require_POST
def update_cart(request):
    session_key = get_session_key(request)
    data = json.loads(request.body)
    item_id = data.get('item_id')
    quantity = int(data.get('quantity', 1))
    if quantity < 1:
        CartItem.objects.filter(id=item_id, session_key=session_key).delete()
    else:
        CartItem.objects.filter(id=item_id, session_key=session_key).update(quantity=quantity)
    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.subtotal() for item in cart_items)
    return JsonResponse({'success': True, 'total': str(total), 'cart_count': cart_items.count()})


def checkout(request):
    session_key = get_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key).select_related('product')
    if not cart_items.exists():
        return redirect('cart')
    total = sum(item.subtotal() for item in cart_items)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        if name and email and address:
            order = Order.objects.create(
                session_key=session_key,
                customer_name=name,
                customer_email=email,
                customer_phone=phone,
                address=address,
                total=total,
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
            cart_items.delete()
            messages.success(request, f'🎉 Order #{order.id} placed successfully! We will contact you at {email}.')
            return redirect('order_success', order_id=order.id)
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_items.count(),
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {'order': order})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            return JsonResponse({'success': True, 'message': 'Thank you! We will get back to you soon.'})
        return JsonResponse({'success': False, 'message': 'Please fill in all fields.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})
