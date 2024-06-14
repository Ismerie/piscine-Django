from django import forms

class EntryForm(forms.Form):
    entry = forms.CharField(label='Nouvelle entrée', max_length=100)
