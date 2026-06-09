from django.urls import path
from django.contrib import admin
from . import views
from .views import MyPasswordResetConfirmView
from .views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm,MyPasswordChangeForm,  MySetPasswordForm
from django.urls import reverse_lazy


urlpatterns = [
    path('', views.home, name='home'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('category/<slug:val>/', views.CategoryView.as_view(), name='category'),
    path('product-detail/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.AddressView.as_view(), name='address'),

    path('updateAddress/<int:pk>/', views.updateAddress.as_view(), name='updateAddress'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('initiate-payment/',views.initiate_payment,name='initiatepayment'),
    path('payment-done/',views.payment_done,name='paymentdone'),
    path('orders/', views.orders, name='orders'),
    path('pluswishlist/', views.plus_wishlist, name='pluswishlist'),
    path('minuswishlist/', views.minus_wishlist, name='minuswishlist'),
    path('search', views.search, name='search'),
    path('wishlist', views.show_wishlist, name='wishlist'),
    path('payment-success/', views.payment_done, name='payment_done'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),

    path(
        'accounts/login/',
        auth_view.LoginView.as_view(
            template_name='app/login.html',
            authentication_form=LoginForm
        ),
        name='login'
    ),

   path(
    'password-reset/',
    auth_view.PasswordResetView.as_view(
        template_name='app/password_reset_form.html',
        form_class=MyPasswordResetForm
    ),
    name='password_reset'
),

path(
    'password-reset/done/',
    auth_view.PasswordResetDoneView.as_view(
        template_name='app/password_reset_done.html'
    ),
    name='password_reset_done'
),
path(
    'reset/<uidb64>/<token>/',
    MyPasswordResetConfirmView.as_view(),
    name='password_reset_confirm'
),


path(
    'password-reset-complete/',
    auth_view.PasswordResetCompleteView.as_view(
        template_name='app/password_reset_complete.html'
    ),
    name='password_reset_complete'
),

path(
    'passwordchange/done/',
    auth_view.PasswordChangeDoneView.as_view(
        template_name='app/password_change_done.html'
    ),
    name='passwordchangedone'
),




]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header ='TIKUS RESTAURANT'
admin.site.site_title ='TIKUS RESTAURANT'
admin.site.site_index_title ='Welcome to TIKUS RESTAURANT'