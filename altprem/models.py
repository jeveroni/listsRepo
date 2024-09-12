from django.db import models

# Create your models here.
class Season(models.Model):
    name = models.CharField(max_length=5, unique=True)
    
    def __str__(self):
        return self.name
    
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key = True)
    
    def __str__(self):
        return self.name
    
class Game(models.Model):
    game_id = models.IntegerField(unique=True)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team_set')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team_set')
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    match_date = models.DateTimeField("Date Of Match")
    season = models.ForeignKey( Season, on_delete=models.CASCADE)
    home_possession = models.FloatField()
    away_possession = models.FloatField()
    home_total_shots = models.IntegerField()
    away_total_shots = models.IntegerField()
    home_on_target = models.IntegerField()
    away_on_target = models.IntegerField()
    home_off_target = models.IntegerField()
    away_off_target = models.IntegerField()
    home_blocked = models.IntegerField()
    away_blocked = models.IntegerField()
    home_passing_percent = models.FloatField()
    away_passing_percent = models.FloatField()
    home_clear_cut_chances = models.IntegerField()
    away_clear_cut_chances = models.IntegerField()
    home_corners = models.IntegerField()
    away_corners = models.IntegerField()
    home_offsides = models.IntegerField()
    away_offsides = models.IntegerField()
    home_tackles = models.FloatField()
    away_tackles = models.FloatField()
    home_aerial_duels = models.FloatField()
    away_aerial_duels = models.FloatField()
    home_saves = models.IntegerField()
    away_saves = models.IntegerField()
    home_fouls_committed = models.IntegerField()
    away_fouls_committed = models.IntegerField()
    home_fouls_won = models.IntegerField()
    away_fouls_won = models.IntegerField()
    home_yellow_cards = models.IntegerField()
    away_yellow_cards = models.IntegerField()
    home_red_cards = models.IntegerField()
    away_red_cards = models.IntegerField()
 
    def __str__(self):
        # return f"{self.game_id}"
        return f"{self.home_team} vs {self.away_team}, {self.season} ({self.game_id})"
    
