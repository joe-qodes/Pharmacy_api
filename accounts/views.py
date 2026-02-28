from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import PatientRegisterSerializer, PharmacyRegisterSerializer, UserSerializer

User = get_user_model()


# ─── REST API ────────────────────────────────────────────────────────────────

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('create', 'register_patient', 'register_pharmacy'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def me(self, request):
        return Response(UserSerializer(request.user).data)


# ─── HTML VIEWS ──────────────────────────────────────────────────────────────

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


def register_patient(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        serializer = PatientRegisterSerializer(data={
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'phone_number': request.POST.get('phone_number', ''),
        })
        if serializer.is_valid():
            user = serializer.save()
            django_login(request, user)
            return redirect('dashboard')
        else:
            for field, errs in serializer.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")
    return render(request, 'register_patient.html')


def register_pharmacy(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        serializer = PharmacyRegisterSerializer(data={
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'phone_number': request.POST.get('phone_number', ''),
            'pharmacy_name': request.POST.get('pharmacy_name'),
            'license_number': request.POST.get('license_number'),
            'address': request.POST.get('address'),
        })
        if serializer.is_valid():
            user = serializer.save()
            django_login(request, user)
            return redirect('dashboard')
        else:
            for field, errs in serializer.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")
    return render(request, 'register_pharmacy.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user:
            django_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    role = request.user.role

    if role == 'pharmacy':
        try:
            pharmacy = request.user.pharmacy_profile
        except Exception:
            pharmacy = None

        if pharmacy and not pharmacy.is_verified:
            return render(request, 'dashboard_pharmacy_pending.html', {'pharmacy': pharmacy})

        from orders.models import Order
        from medications.models import PharmacyMedication

        pending_orders = Order.objects.filter(pharmacy=pharmacy, status='pending') if pharmacy else []
        all_orders = Order.objects.filter(pharmacy=pharmacy) if pharmacy else []
        inventory = PharmacyMedication.objects.filter(pharmacy=pharmacy).select_related('medication') if pharmacy else []

        return render(request, 'dashboard_pharmacy.html', {
            'pharmacy': pharmacy,
            'pending_orders': pending_orders,
            'all_orders': all_orders,
            'inventory': inventory,
        })

    elif role == 'patient':
        from orders.models import Order
        my_orders = Order.objects.filter(patient=request.user).select_related('pharmacy', 'medication')
        return render(request, 'dashboard_patient.html', {
            'my_orders': my_orders,
        })

    else:  # admin
        return render(request, 'dashboard_admin.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def search_medications(request):
    if not request.user.is_authenticated:
        return redirect('login')

    from medications.models import PharmacyMedication
    results = []
    query = request.GET.get('q', '').strip()
    pharmacy_filter = request.GET.get('pharmacy', '').strip()

    if query or pharmacy_filter:
        qs = PharmacyMedication.objects.select_related('medication', 'pharmacy').filter(stock__gt=0)
        if query:
            qs = qs.filter(medication__name__icontains=query)
        if pharmacy_filter:
            qs = qs.filter(pharmacy__name__icontains=pharmacy_filter)
        results = qs

    from pharmacies.models import Pharmacy
    pharmacies = Pharmacy.objects.filter(is_verified=True)

    return render(request, 'search.html', {
        'results': results,
        'query': query,
        'pharmacy_filter': pharmacy_filter,
        'pharmacies': pharmacies,
    })


def place_order(request):
    if not request.user.is_authenticated or request.user.role != 'patient':
        return redirect('login')

    if request.method == 'POST':
        from medications.models import PharmacyMedication
        from orders.models import Order

        pm_id = request.POST.get('pharmacy_medication_id')
        try:
            pm = PharmacyMedication.objects.select_related('pharmacy', 'medication').get(id=pm_id)
        except PharmacyMedication.DoesNotExist:
            messages.error(request, 'Medication not found.')
            return redirect('search')

        if pm.stock < 1:
            messages.error(request, 'This medication is out of stock.')
            return redirect('search')

        Order.objects.create(
            patient=request.user,
            pharmacy=pm.pharmacy,
            medication=pm.medication,
            pharmacy_medication=pm,
            status='pending',
        )
        messages.success(request, f'Order placed for {pm.medication.name} at {pm.pharmacy.name}!')
        return redirect('dashboard')

    return redirect('search')