from django import forms

class DropdownMovieForm(forms.Form):
    movie = forms.ChoiceField(choices=[], label='Select a Movie to remove')

    def __init__(self, choices, *args, **kwargs):
        super(DropdownMovieForm, self).__init__(*args, **kwargs)
        self.fields['movie'].choices = choices