from django import forms
from .models import Season, Team, Game


class SeasonForm(forms.ModelForm):
    
    class Meta:
        model = Season
        fields = ('name',)
        
class TeamForm(forms.ModelForm):
    
    class Meta:
        model = Team
        fields = ('name',)
        
class GameForm(forms.ModelForm):
    
    class Meta:
        model = Game
        fields = ()