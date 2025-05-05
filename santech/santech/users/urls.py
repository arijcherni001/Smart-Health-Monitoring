from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('appointment', views.appointment, name='appointment'),
    path('feature', views.feature, name='feature'),
    path('team', views.team, name='team'),
    path('testimonial', views.testimonial, name='testimonial'),
    path('404', views.page_not_found, name='404'),
    path('service', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'), name='password_reset_complete'),

    path('logout/', views.logout_view, name='logout'), 
    path('diagnostic/', views.diagnostic_view, name='diagnostic'),  
    path('api/latest-data/',views.latest_data_api, name="latest_data_api"),
]
