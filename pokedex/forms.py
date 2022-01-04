from django import forms
class PokemonForm(forms.Form):
    pokemon = forms.CharField(label='pokemon', max_length=100)