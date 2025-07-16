from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

DAYS_OF_WEEK = [
    ('sat', 'Saturday'),
    ('sun', 'Sunday'),
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thu', 'Thursday'),
    ('fri', 'Friday'),
]

class Specialty(models.Model):
    name = models.CharField(max_length=100)

class BarberUserManager(BaseUserManager):
    def create_user(self, phone, firstname, lastname, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone number is required')
        phone = str(phone)
        user = self.model(phone=phone, firstname=firstname, lastname=lastname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, firstname, lastname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(phone, firstname, lastname, password, **extra_fields)


class BarberUser(AbstractBaseUser):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=150)
    phone = models.PositiveIntegerField(max_length=11)
    is_barber = models.BooleanField(default=False)
    bio = models.TextField()
    specialties = models.ManyToManyField(Specialty, related_name='barbers')


initial_specialties = [
    "Haircut", "Shaving with razor", "Eyebrow shaping", "Hair coloring",
    "Highlights", "Keratin treatment", "Bleaching", "Braiding", "Hair Botox", "Updo", "Bridal makeup"
]

for name in initial_specialties:
    Specialty.objects.get_or_create(name=name)


class WorkingTime(models.Model):
    barber = models.ForeignKey(BarberUser, related_name="workingtime", on_delete=models.CASCADE)
    days = models.CharField(choices=DAYS_OF_WEEK, max_length=10)
    starttime = models.TimeField()
    endtime = models.TimeField()
    
    class Meta:
        unique_together = ('barber', 'day')
    
    def __str__(self):
        return f"{self.barber}"
    