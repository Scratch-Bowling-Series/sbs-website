from accounts import forms
from accounts.forms import User


class BowlersSearch(forms.Form):
    search_args = forms.CharField()