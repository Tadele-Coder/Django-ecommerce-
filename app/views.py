from django.db.models import Count
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import logout
from django.shortcuts import render, redirect,  get_object_or_404
from django.views import View
from .models import Product, Customer, Cart,  OrderPlaced, Wishlist

from .forms import CustomerRegistrationForm, CustomerProfileForm, MyPasswordChangeForm,  MySetPasswordForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import telebirr
import uuid
from django.conf import settings


# Create your views here.
def home(request):
    # totalitem = 0
    wishlist=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        # wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/home.html', locals())


def about(request):
    totalitem = 0
    # wishlist=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        # wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/about.html', locals())


def contact(request):
    totalitem = 0
    # wishlist=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        # wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/contact.html', locals())

@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request, val):

        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html', locals())

@method_decorator(login_required, name='dispatch')      
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title =Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/category.html', locals())

@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)

        # IMPORTANT FIX
        product.final_price = product.selling_price - product.discounted_price

        wishlist = Wishlist.objects.filter(product=product, user=request.user)

        totalitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()

        return render(request, 'app/productdetail.html', locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful")
            return redirect('login') 
        else:
            messages.warning(request, "Invalid registration data")

        return render(request, 'app/customerregistration.html', locals())

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()

        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)

        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(
                user=user,
                name=name,
                locality=locality,
                mobile=mobile,
                city=city,
                state=state,
                zipcode=zipcode
            )
            reg.save()

            messages.success(request, "Congratulations! Profile saved successfully.")
        else:
            messages.warning(request, "Invalid input data.")

        return render(request, 'app/profile.html', locals())

@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        add = Customer.objects.filter(user=request.user)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/address.html', locals())

class updateAddress(View):

    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html', locals())

    def post(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(request.POST, instance=add)

        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congradulation! Profile Update Successfully")
        else:
            messages.warning(request, "invalid Input data")

        return redirect('address')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')



@login_required
def add_to_cart(request):

    if request.method == "POST":

        user = request.user
        product_id = request.POST.get('prod_id')

        product = get_object_or_404(Product, id=product_id)

        Cart.objects.create(user=user, product=product)

        return redirect('/cart')

    return redirect('/')

def show_cart(request):
    cart = Cart.objects.filter(user=request.user)

    amount = 0

    for item in cart:
        item.current_price = (
            item.product.selling_price - item.product.discounted_price
        ) * item.quantity

        amount += item.current_price

    transport = 250
    totalamount = amount + transport

    return render(request, 'app/addtocart.html', {
        'cart': cart,
        'amount': amount,
        'transport': transport,
        'totalamount': totalamount,
    })

class checkout(View):
    def get(self, request):

        cart_items = Cart.objects.filter(user=request.user)
        totalitem = cart_items.count()

        original_amount = 0
        discount_amount = 0

        for p in cart_items:
            original_amount += p.product.selling_price * p.quantity
            discount_amount += p.product.discounted_price * p.quantity

        current_amount = original_amount - discount_amount

        transport = 250
        totalamount = current_amount + transport

        return render(request, 'app/checkout.html', {
            'cart_items': cart_items,
            'totalitem': totalitem,

            'original_amount': original_amount,
            'discount_amount': discount_amount,
            'current_amount': current_amount,

            'transport': transport,
            'totalamount': totalamount,
        })
        
@login_required
def plus_cart(request):

    prod_id = request.GET.get('prod_id')

    cart_item, created = Cart.objects.get_or_create(
        product_id=prod_id,
        user=request.user
    )

    cart_item.quantity += 1
    cart_item.save()

    cart = Cart.objects.filter(user=request.user)

    amount = sum(
        (p.product.selling_price - p.product.discounted_price) * p.quantity
        for p in cart
    )

    totalamount = amount + 250

    return JsonResponse({
        'quantity': cart_item.quantity,
        'amount': amount,
        'totalamount': totalamount
    })

@login_required
def minus_cart(request):

    prod_id = request.GET.get('prod_id')

    cart_item = Cart.objects.get(product_id=prod_id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    cart = Cart.objects.filter(user=request.user)

    amount = sum(
        (p.product.selling_price - p.product.discounted_price) * p.quantity
        for p in cart
    )

    totalamount = amount + 250

    return JsonResponse({
        'quantity': cart_item.quantity if cart_item.id else 0,
        'amount': amount,
        'totalamount': totalamount
    })

@login_required
def remove_cart(request):

    prod_id = request.GET.get('prod_id')

    Cart.objects.filter(product_id=prod_id, user=request.user).delete()

    cart = Cart.objects.filter(user=request.user)

    amount = sum(
        (p.product.selling_price - p.product.discounted_price) * p.quantity
        for p in cart
    )

    totalamount = amount + 250

    return JsonResponse({
        'amount': amount,
        'totalamount': totalamount,
        'quantity': 0
    })

@login_required
def initiate_payment(request):

    amount = request.POST.get('totamount')

    messages.success(request, f"Telebirr Test Payment Successful: ETB {amount}")

    return redirect('payment_done')
    
from django.contrib.auth.decorators import login_required

@login_required
def payment_done(request):

    user = request.user
    cart_items = Cart.objects.filter(user=user)

    for item in cart_items:

        unit_price = item.product.selling_price - item.product.discounted_price

        OrderPlaced.objects.create(
            user=user,
            product=item.product,
            quantity=item.quantity,
            price=unit_price,   # ✅ FIXED HERE
            status="Pending"
        )

    cart_items.delete()

    return render(request, 'app/payment_success.html')

def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishlist =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request, 'app/wishlist.html', locals())


@login_required
def plus_wishlist(request):

    if request.method == 'GET':

        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user

        Wishlist.objects.get_or_create(
            user=user,
            product=product
        )

        data = {
            'message': 'Wishlist Added Successfully',
        }

        return JsonResponse(data)


@login_required
def minus_wishlist(request):

    if request.method == 'GET':

        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user

        Wishlist.objects.filter(
            user=user,
            product=product
        ).delete()

        data = {
            'message': 'Wishlist Remove Successfully',
        }

        return JsonResponse(data)

@login_required
def search(request):
    query = request.GET.get('search')

    totalitem = 0
    wishlist = 0

    if request.user.is_authenticated:
        totalitem = Wishlist.objects.filter(user=request.user).count()
        wishlist = totalitem

    
    product = Product.objects.none()

   
    if query:
        product = Product.objects.filter(Q(title__icontains=query))

    return render(request, 'app/search.html', {
        'product': product,
        'query': query,
        'totalitem': totalitem,
        'wishlist': wishlist,
    })

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'app/password_reset_confirm.html'
    form_class = MySetPasswordForm
    



