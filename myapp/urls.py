from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .forms import LoginForm,PasswordChangeForm


urlpatterns = [
    path('', views.home,name='home'),

    path('productdetail/<int:pk>', views.productdetail, name='productdetail'),
    
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html',next_page='/',authentication_form=LoginForm),name='login'),

    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name="logout"),

    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='passwordchange.html',form_class=PasswordChangeForm),name='passwordchange'),
    
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),

    path('filter/', views.make_filter, name='filter'),

    # path('cart/', views.add_to_cart, name='add-to-cart'),
    path('profile/', views.profile, name='profile'),
    # path('changepassword/', views.change_password, name='changepassword'),

    # path('filter/<slug:data>', views.filter, name='filter-data'),

    # path('checkout/', views.checkout, name='checkout'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
