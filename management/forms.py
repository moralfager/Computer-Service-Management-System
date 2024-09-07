
import datetime
from django.utils import timezone
from .models import Order, Service, Technician, OrderMaterial, Material
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TechnicianLoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Қолданушының аты",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пайдаланушы атыңызды енгізіңіз'})
    )
    password = forms.CharField(
        label="Құпия сөз",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Құпия сөзіңізді енгізіңіз'})
    )
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service_type', 'service', 'technician', 'description', 'completion_date']
        widgets = {
            'completion_date': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today() + datetime.timedelta(days=1)}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['technician'].queryset = Technician.objects.none()

        if 'service' in self.data:
            try:
                service_id = int(self.data.get('service'))
                self.fields['technician'].queryset = Technician.objects.filter(service_id=service_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Technician queryset
        elif self.instance.pk:
            self.fields['technician'].queryset = self.instance.service.technician_set.order_by('name')



class TechnicianRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100, help_text='Enter your full name')
    service_id = forms.ModelChoiceField(queryset=Service.objects.all(), empty_label="Choose Service", help_text='Select the service you are skilled at')

    class Meta:
        model = User
        fields = ('username', 'name', 'service_id', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        service = self.cleaned_data['service_id']
        technician = Technician.objects.create(user=user, name=self.cleaned_data['name'], service=service)
        return user


class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class OrderMaterialForm(forms.ModelForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    quantity_used = forms.IntegerField(min_value=1)

    class Meta:
        model = OrderMaterial
        fields = ['material', 'quantity_used']

class MaterialOrderForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'model_compatibility', 'status', 'expiration_date', 'quantity']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TechnicianProfileForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ['name', 'service', 'service_fee']
