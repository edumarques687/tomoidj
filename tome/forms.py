from django.forms import ModelForm
from .models import Tome


class TomeForm(ModelForm):
    class Meta:
        model = Tome
        fields = ['name']
