from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
    ]
    
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='F', 
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username