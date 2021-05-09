from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils import timezone

actions = (
    ('Creation', 'Creation'),
    ('Deletion', 'Deletion')
)


# Create your models here.


class UserRegistration(AbstractUser):
    user_image = models.ImageField(upload_to="uploads/", blank=True, null=True)

class Todomodel(models.Model):
    name = models.CharField(max_length=120)
    address = models.TextField()
    contact = models.IntegerField()

    def __str__(self):
        return (self.name)


class LogHistory(models.Model):
    action = models.CharField(max_length=50, choices=actions)
    timestamp = models.DateTimeField()
    todo = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()
        return super(LogHistory, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.todo)
