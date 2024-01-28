from django.urls import path, reverse_lazy
from myapp import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm

app_name = 'myapp'

urlpatterns = [
    path('', views.home,name='home'),

    path('filter/', views.make_filter, name='filter'),

    path('productdetail/<int:pk>', views.productdetail, name='productdetail'),
    path('cart/productdetail/<int:pk>', views.productdetail, name='cartproductdetail'),
    
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html',next_page='/',authentication_form=LoginForm),name='login'),

    path('logout/',auth_views.LogoutView.as_view(next_page='/'),name="logout"),

    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='passwordchange.html',form_class=MyPasswordChangeForm,success_url ='/passwordchangedone/'),name='passwordchange'),
    
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),

    path ('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html',email_template_name = 'password_reset_email.html',success_url=reverse_lazy('myapp:password_reset_done'),form_class=MyPasswordResetForm),name='password_reset'),

    path ('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),

    path ('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',success_url=reverse_lazy('myapp:password_reset_complete'),form_class = MySetPasswordForm),name='password_reset_confirm'),

    path ('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('helpsupport/', views.ReportView.as_view(), name='helpsupport'),

    path('search/', views.product_search, name="search"),


    path('buynow/', views.buy_now, name='buynow'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('cart/', views.show_cart, name='showcart'),

    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),

    path('placeorder/',views.place_order,name='placeorder'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('orders/',views.order_done,name='orders'),

    path('address/', views.address, name='address'),
    
    path('categories/', views.categories, name='categories'),
    path('products/<int:category>/', views.products, name='products_category'),
    path('products/', views.products, name='products'),
    path('about/', views.about, name='about'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
