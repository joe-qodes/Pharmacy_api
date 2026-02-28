from django.urls import path
from .views import (
    home,
    register_page,
    login_page,
    dashboard,
    logout_view
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
]