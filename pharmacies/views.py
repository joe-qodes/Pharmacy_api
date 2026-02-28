from rest_framework import viewsets, permissions
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pharmacy
from .serializers import PharmacySerializer
from medications.models import PharmacyMedication, Medication


class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# HTML: update stock for a medication in pharmacy inventory
def update_stock(request, pm_id):
    if not request.user.is_authenticated or request.user.role != 'pharmacy':
        return redirect('login')

    try:
        pharmacy = request.user.pharmacy_profile
    except Exception:
        return redirect('dashboard')

    pm = get_object_or_404(PharmacyMedication, id=pm_id, pharmacy=pharmacy)

    if request.method == 'POST':
        try:
            stock = int(request.POST.get('stock', pm.stock))
            price = float(request.POST.get('price', pm.price))
            pm.stock = stock
            pm.price = price
            pm.save()
            messages.success(request, f'Updated {pm.medication.name} successfully.')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid stock or price value.')

    return redirect('dashboard')


# HTML: add a new medication to pharmacy inventory
def add_medication(request):
    if not request.user.is_authenticated or request.user.role != 'pharmacy':
        return redirect('login')

    try:
        pharmacy = request.user.pharmacy_profile
    except Exception:
        return redirect('dashboard')

    if not pharmacy.is_verified:
        messages.error(request, 'Your pharmacy must be verified before adding medications.')
        return redirect('dashboard')

    medications = Medication.objects.all()

    if request.method == 'POST':
        med_id = request.POST.get('medication_id')
        try:
            stock = int(request.POST.get('stock', 0))
            price = float(request.POST.get('price', 0))
            medication = Medication.objects.get(id=med_id)

            pm, created = PharmacyMedication.objects.get_or_create(
                pharmacy=pharmacy,
                medication=medication,
                defaults={'stock': stock, 'price': price}
            )
            if not created:
                pm.stock = stock
                pm.price = price
                pm.save()
                messages.success(request, f'{medication.name} stock updated.')
            else:
                messages.success(request, f'{medication.name} added to inventory.')
        except (Medication.DoesNotExist, ValueError, TypeError):
            messages.error(request, 'Invalid medication or values.')

        return redirect('dashboard')

    return render(request, 'add_medication.html', {'medications': medications})