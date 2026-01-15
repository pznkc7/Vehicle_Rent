from django import forms
from .models import Vehicle


class VehicleApplicationForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'vehicle_name',
            'vehicle_type',
            'pickup_address',
            'latitude',
            'longitude',
            'price_per_hour',
            'price_per_day',
            'image',
            'description',
        ]

        widgets = {
            'vehicle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),

            # ✅ Map-controlled fields
            'pickup_address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Select location on map',
                }
            ),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),

            'price_per_hour': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }

    # ✅ HARD VALIDATION (IMPORTANT)
    def clean(self):
        cleaned_data = super().clean()

        lat = cleaned_data.get('latitude')
        lng = cleaned_data.get('longitude')

        if not lat or not lng:
            raise forms.ValidationError(
                "Please select the pickup location on the map."
            )

        return cleaned_data
