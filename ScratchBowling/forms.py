from django import forms


class BowlersSearch(forms.Form):
    search_args = forms.CharField(max_length=100)