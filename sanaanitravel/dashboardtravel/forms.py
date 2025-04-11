# forms.py
from django import forms
from .models import Contact
from .models import PrivateTripRequest, PrivateTripApproval, PrivateTripPayment, City, Nationality


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['customer_passport_number'].required = False
        
        
        self.check_passport_requirement()
    
    def check_passport_requirement(self):
        try:
            yemen = Nationality.objects.get(name='اليمن')
            departure = self.data.get('departure') or self.initial.get('departure')
            destination = self.data.get('destination') or self.initial.get('destination')
            
            if departure and destination:
                departure_city = City.objects.get(id=int(departure))
                destination_city = City.objects.get(id=int(destination))
                
              
                if not (departure_city.nationality == yemen and destination_city.nationality == yemen):
                    self.fields['customer_passport_number'].required = True
                    self.fields['customer_passport_number'].widget.attrs['required'] = 'required'
        except (Nationality.DoesNotExist, City.DoesNotExist, ValueError, TypeError):
            pass


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