from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from inventory.models import *

class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'material_type', 'material_code', 'stock_quantity', 'unit_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('material_type', css_class='form-group col-md-4 mb-0'),
                Column('material_code', css_class='form-group col-md-4 mb-0'),
                css_class='row'
            ),
            Row(
                Column('stock_quantity', css_class='form-group col-md-4 mb-0'),
                Column('unit_price', css_class='form-group col-md-4 mb-0'),
                css_class='row mb-4'
            ),
            Submit('submit', 'ADD')
        )