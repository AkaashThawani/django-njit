from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

User = get_user_model()


# Create your models here.

class Location(models.Model):
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_location} to {self.to_location} at {self.timestamp}"


class SearchLocation(models.Model):
    TRAVEL_MODE_CHOICES = [
        ('WALKING', 'Walking'),
        ('DRIVING', 'Driving'),
        ('CYCLING', 'Cycling'),
    ]
    from_location_name = models.CharField(max_length=100)
    from_location_lat = models.FloatField()
    from_location_lng = models.FloatField()
    to_location_name = models.CharField(max_length=100)
    to_location_lat = models.FloatField()
    to_location_lng = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    travel_mode = models.CharField(max_length=10, choices=TRAVEL_MODE_CHOICES)
    search_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,)  

    def __str__(self):
        return f"{self.from_location_name} to {self.to_location_name} at {self.timestamp}"


class CampusEvent(models.Model):
    campus_name = models.CharField(max_length=100)
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=200)
    event_description = models.TextField()
    event_image = models.ImageField(upload_to='event_images/')
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)
    organizers_name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50)
    location = models.CharField(max_length=200)  

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically generate a slug from the event name
        self.slug = slugify(self.event_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event_name} at {self.campus_name} ({self.start_time} to {self.end_time})"


class Building(models.Model):
    build_name = models.CharField(max_length=100)
    build_img = models.ImageField(_("Building Image"), upload_to='building_images/',
                                  height_field=None, width_field=None, max_length=None)
    build_description = models.TextField()

    def __str__(self):
        return self.build_name


class Feedback(models.Model):
    user_name = models.CharField(max_length=100)
    comment = models.TextField()
    admin_comment = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name}'s Feedback"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s session"


class Login(models.Model):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    login_time = models.DateTimeField(auto_now_add=True)
    # Add more fields as needed

    def __str__(self):
        return f"{self.user.username}'s {self.get_user_type_display()} login at {self.login_time}"
