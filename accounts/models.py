from django.db import models
from django.contrib.auth.models import User


# class User(AbstractUser):
#     photo = models.ImageField()
#     date_of_birth = models.DateTimeField()
#     address = models.TextField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    photo = models.ImageField(upload_to='users/', blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    bio = models.TextField()

    def __str__(self):
        return f"{self.user.username} profili"
