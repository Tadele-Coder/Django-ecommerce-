from .models import Cart, Wishlist

def nav_items(request):
    cart_count = 0
    wishlist_count = 0

    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return {
        'totalitem': cart_count,
        'wishlist_count': wishlist_count
    }