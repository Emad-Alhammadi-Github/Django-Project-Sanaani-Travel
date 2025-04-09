# forms.py
from django import forms
from .models import Contact
from .models import PrivateTripRequest, PrivateTripApproval, PrivateTripPayment

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']




class PrivateTripRequestForm(forms.ModelForm):
    class Meta:
        model = PrivateTripRequest
        fields = [
            'trip_type', 'departure', 'destination', 
            'vehicle_type', 'passenger_count', 
            'trip_date', 'trip_time', 'special_requests',
            'customer_name', 'customer_id_number', 'identify_img',
            'customer_passport_number', 'customer_phone', 
            'customer_email', 'customer_nationality'
        ]
        widgets = {
            'trip_date': forms.DateInput(attrs={'type': 'date'}),
            'trip_time': forms.TimeInput(attrs={'type': 'time'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
            'customer_id_number': forms.TextInput(attrs={'placeholder': 'رقم الهوية'}),
            'customer_passport_number': forms.TextInput(attrs={'placeholder': 'رقم الجواز (اختياري)'}),
        }
# class PrivateTripRequestForm(forms.ModelForm):
#     class Meta:
#         model = PrivateTripRequest
#         fields = [
#             'trip_type', 'departure', 'destination', 
#             'vehicle_type', 'passenger_count', 
#             'trip_date', 'trip_time', 'special_requests',
#             'customer_phone', 'customer_email', 'customer_nationality'
#         ]
#         widgets = {
#             'trip_date': forms.DateInput(attrs={'type': 'date'}),
#             'trip_time': forms.TimeInput(attrs={'type': 'time'}),
#             'special_requests': forms.Textarea(attrs={'rows': 3}),
#         }

class TripApprovalForm(forms.ModelForm):
    class Meta:
        model = PrivateTripApproval
        fields = ['price', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = PrivateTripPayment
        fields = ['payment_method']