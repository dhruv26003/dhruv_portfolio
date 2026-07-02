from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "Your Full Name",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "Your Email Address",
                    "required": True,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "Your Phone Number (Optional)",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "Subject",
                    "required": True,
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "Tell me about your project or inquiry...",
                    "rows": 5,
                    "required": True,
                }
            ),
        }
