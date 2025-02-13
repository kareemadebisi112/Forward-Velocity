from django.forms import ModelForm
from django import forms
from .models import Lead
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

class LeadForm(ModelForm):
    CHOICES = (
        ('AI Features', 'AI Features'),
        ('Web Hosting', 'Web Hosting'),
        ('Web Design', 'Web Design'),
        ('Digital Marketing', 'Digital Marketing'),
        ('Other', 'Other'),
    )
    service = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple, label='Service(s)')
    message = forms.CharField(widget=forms.Textarea, required=True, label='Tell us more about your project.')
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = Lead
        fields = ['name', 'email', 'service', 'message']