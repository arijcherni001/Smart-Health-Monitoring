from django.db import models

class Data(models.Model):
    temperature = models.FloatField()
    oxygene = models.FloatField()
    bpm = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temp: {self.temperature}°C, Oxygene: {self.oxygene}%, BPM: {self.bpm} @ {self.timestamp}"
