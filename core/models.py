from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    id: models.AutoField = models.AutoField(primary_key=True)
    ADMIN = 'Admin'
    TECHNICIAN = 'Technician'
    CLIENT = 'Client'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (TECHNICIAN, 'Technician'),
        (CLIENT, 'Client'),
    ]

    email: models.EmailField = models.EmailField(unique=True)
    phone_number: models.CharField = models.CharField(max_length=20)
    role: models.CharField = models.CharField(max_length=50, choices=ROLE_CHOICES)
    name: models.CharField = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    
    # Add other fields as necessary

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number', 'role']

    def __str__(self):
        return self.name



class Profile(models.Model):
    user: models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    address: models.CharField = models.CharField(max_length=255)
    profile_picture: models.CharField = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth: models.DateField = models.DateField()
    gender: models.CharField = models.CharField(max_length=10)
    role: models.CharField = models.CharField(max_length=50, choices=User.ROLE_CHOICES)

    def __str__(self):
        return f'{self.user.name} Profile'


class Task(models.Model):
    PENDING = 'Pending'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    ]

    title: models.CharField = models.CharField(max_length=255)
    date: models.DateField = models.DateField()
    time: models.TimeField = models.TimeField()
    status: models.CharField = models.CharField(max_length=50, choices=STATUS_CHOICES)
    technician_assigned: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', limit_choices_to={'role': 'Technician'})
    ai_predicted_fault: models.CharField = models.CharField(max_length=255)
    problem: models.OneToOneField = models.OneToOneField('Problem', on_delete=models.CASCADE)
    grid: models.ForeignKey = models.ForeignKey('Grid', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Problem(models.Model):
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_problems', limit_choices_to={'role': 'Client'})
    name: models.CharField = models.CharField(max_length=255)
    email: models.EmailField = models.EmailField()
    location: models.CharField = models.CharField(max_length=255)
    description: models.TextField = models.TextField()

    def __str__(self):
        return self.name


class Grid(models.Model):
    total_clients: models.IntegerField = models.IntegerField()
    total_networks: models.IntegerField = models.IntegerField()
    energy_allocated: models.FloatField = models.FloatField()
    status: models.CharField = models.CharField(max_length=50, choices=[('Operational', 'Operational'), ('Down', 'Down')])

    def __str__(self):
        return f'Grid {self.id}'
