from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.date})"
