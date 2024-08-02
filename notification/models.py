from django.db import models

# Create your models here.

class Notification(models.Model):
    title = models.TextField()
    message = models.TextField()

    def __str__(self):
        return self.message