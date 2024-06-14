from django import forms
from .models import People

class MovieFilterForm(forms.Form):
    min_release_date = forms.DateField(label='Movies minimum release date')
    max_release_date = forms.DateField(label='Movies maximum release date')
    planet_diameter_greater_than = forms.IntegerField(label='Planet diameter greater than')

    def __init__(self, *args, **kwargs):
        super(MovieFilterForm, self).__init__(*args, **kwargs)
        # Getting distinct values for gender from People model
        gender_choices = People.objects.values_list('gender', flat=True).distinct()
        gender_choices = [(gender, gender) for gender in gender_choices if gender]
        self.fields['character_gender'] = forms.ChoiceField(choices=gender_choices, label='Character gender')