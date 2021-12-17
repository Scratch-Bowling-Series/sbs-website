
from django import forms
from tournaments.models import Tournament



class CreateTournament(forms.ModelForm):
    tournament_date = forms.DateField(required=False)
    tournament_time = forms.TimeField(required=False)
    picture = forms.ImageField(required=False)
    center = forms.UUIDField(required=False)
    format = forms.UUIDField(required=False)
    entry_fee = forms.FloatField(required=False)
    total_games = forms.IntegerField(required=False)
    placements = forms.JSONField(required=False)
    class Meta:
        model = Tournament
        fields = ['name', 'description', 'datetime', 'picture', 'center', 'format', 'entry_fee', 'total_games', 'placements']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class ModifyTournament(forms.ModelForm):
    tournament_date = forms.DateField(required=False)
    tournament_time = forms.TimeField(required=False)
    picture = forms.ImageField(required=False)
    center = forms.UUIDField(required=False)
    format = forms.UUIDField(required=False)
    entry_fee = forms.FloatField(required=False)
    total_games = forms.IntegerField(required=False)
    placements = forms.JSONField(required=False)
    class Meta:
        model = Tournament
        fields = ['name', 'description', 'datetime', 'picture', 'center', 'format', 'entry_fee', 'total_games', 'placements']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
