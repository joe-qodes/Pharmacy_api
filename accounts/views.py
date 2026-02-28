from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    

def home(request):
    return render(request, 'home.html')

def register_page(request):
    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password'],
            role=request.POST['role']
        )
        return redirect('login_page')

    return render(request, 'register.html')


def login_page(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            django_login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login_page')

    return render(request, 'dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('home')