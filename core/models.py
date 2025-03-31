from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.forms import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user  # Profile will be created by the signal

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
    user: models.OneToOneField = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Better practice than direct User reference
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='unique_user_profile'
            )
        ]
    address: models.CharField = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        max_length=255
    )
    date_of_birth:models.DateField = models.DateField(null=True, blank=True)
    gender:models.CharField = models.CharField(max_length=10, null=True, blank=True)
    role: models.CharField = models.CharField(max_length=50, choices=User.ROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.user.name} Profile'
    def clean(self):
        """Additional validation before saving"""
        if not self.user_id:
            raise ValidationError("Profile must be associated with a user")
        if Profile.objects.filter(user_id=self.user_id).exclude(pk=self.pk).exists():
            raise ValidationError("A profile already exists for this user")

    def save(self, *args, **kwargs):
        self.full_clean()  # Runs clean() validation
        super().save(*args, **kwargs)
    
    # def save(self, *args, **kwargs):
    #     # Delete old file when updating
    #     try:
    #         old = Profile.objects.get(pk=self.pk)
    #         if old.profile_picture != self.profile_picture:
    #             old.profile_picture.delete(save=False)
    #     except Profile.DoesNotExist:
    #         pass
    #     super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Delete file when profile is deleted
        if self.profile_picture:
            self.profile_picture.delete(save=False)
        super().delete(*args, **kwargs)

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
