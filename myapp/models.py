from django.db import models
from django.utils import timezone

class FoodItem(models.Model):
   
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    date_consumed = models.DateField(default=timezone.now) # Automatically sets to today's date

    def __str__(self):
       
        return f"{self.name} ({self.calories} calories) on {self.date_consumed}"

    class Meta:
        ordering = ['-date_consumed', 'name']
