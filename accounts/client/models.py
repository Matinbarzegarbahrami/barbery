from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class ClientUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number must be set")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(phone, password, **extra_fields)



class ClientUser(AbstractBaseUser):
    ages = [(str(i), str(i)) for i in range(1, 100)]
    username = None
    firstname = models.CharField(max_length=100,blank=True, null=True)
    lastname = models.CharField(max_length=150,blank=True, null=True)
    phone = models.CharField(max_length=11, unique=True)
    bio = models.TextField(blank=True, null=True)
    age = models.CharField(choices=ages, max_length=20)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'phone'
    
    objects = ClientUserManager()
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.phone