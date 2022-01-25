from django.db import models

# Create your models here.

class Team(models.Model):
    pokemon1 = models.IntegerField(null=True)
    pokemon2 = models.IntegerField(null=True)
    pokemon3 = models.IntegerField(null=True)
    pokemon4 = models.IntegerField(null=True)
    pokemon5 = models.IntegerField(null=True)
    pokemon6 = models.IntegerField(null=True)
    
def __str__(self):
        return f"{self.pokemon1}:{self.pokemon2}:{self.pokemon3}:{self.pokemon4},{self.pokemon5},{self.pokemon6}"