from django.db import models

# Create your models here.

class Team(models.Model):
    pokemon1 = models.IntegerField(max_length=4, null=True)
    pokemon2 = models.IntegerField(max_length=4, null=True)
    pokemon3 = models.IntegerField(max_length=4, null=True)
    pokemon4 = models.IntegerField(max_length=4, null=True)
    pokemon5 = models.IntegerField(max_length=4, null=True)
    pokemon6 = models.IntegerField(max_length=4, null=True)
    
def __str__(self):
        return f"{self.pokemon1}:{self.pokemon2}:{self.pokemon3}:{self.pokemon4},{self.pokemon5},{self.pokemon6}"