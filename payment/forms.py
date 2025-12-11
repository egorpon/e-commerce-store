from django import forms
from .models import ShippingAddress
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = (
            "full_name",
            "email",
            "city",
            "address1",
            "address2",
            "state",
            "zipcode",
        )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update({
            "placeholder": "Full name*",
            "id": "name",
        })
        self.fields["email"].widget.attrs.update({
            "placeholder": "Email address*",
            "id": "email",
        })
        self.fields["address1"].widget.attrs.update({
            "placeholder": "Address 1*",
            "id": "address1",
        })
        self.fields["address2"].widget.attrs.update({
            "placeholder": "Address 2 (Optional)",
            "id": "address2",
        })
        self.fields["city"].widget.attrs.update({
            "placeholder": "City*",
            "id": "city",
        })
        self.fields["state"].widget.attrs.update({
            "placeholder": "State (Optional)",
            "id": "state",
        })
        self.fields["zipcode"].widget.attrs.update({
            "placeholder": "Zip code (Optional)",
            "id": "zipcode",
        })

        for field in self.fields:
            self.fields[field].label = ""
            self.fields[field].widget.attrs.update({
                "class": "form-control my-3"
            })

