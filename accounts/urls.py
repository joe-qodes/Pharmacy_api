from django.urls import path
from .views import (
    home,
    register_patient,
    register_pharmacy,
    login_page,
    dashboard,
    logout_view,
    search_medications,
    place_order,
)

urlpatterns = [
    path('', home, name='home'),
    path('register/patient/', register_patient, name='register_patient'),
    path('register/pharmacy/', register_pharmacy, name='register_pharmacy'),
    path('login/', login_page, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('search/', search_medications, name='search'),
    path('order/place/', place_order, name='place_order'),
]