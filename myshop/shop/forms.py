from django.forms import ModelForm
from shop.models import DataView, Run

class DataViewForm(ModelForm):
    class Meta:
        model = DataView
        fields = '__all__'

class RunForm(ModelForm):
    class Meta:
        model = Run
        fields = '__all__'