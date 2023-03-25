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

    # path('cart/', views.add_to_cart, name='add-to-cart'),
    # path('changepassword/', views.change_password, name='changepassword'),

    # path('filter/<slug:data>', views.filter, name='filter-data'),

    path('address/', views.address, name='address'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
