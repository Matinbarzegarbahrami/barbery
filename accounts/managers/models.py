from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class ManagerUser(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=100,blank=True, null=True)
    lastname = models.CharField(max_length=150,blank=True, null=True)
    phone = models.CharField(max_length=11, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    class Meta:
        ordering = ["phone"]
    
    def __str__(self):
        return self.phone