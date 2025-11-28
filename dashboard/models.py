from django.db import models
from django.contrib.auth.models import User

PERMISSION_CHOICES = [
    ('dashboard', 'Dashboard'),
    ('pending_jobs', 'Pending Jobs'),
    ('pending_properties', 'Pending Properties'),
    ('messages', 'Messages'),
    ('reports', 'Reports'),
]
STATUS_CHOICES = [
    ('active', 'Active'),
    ('offline', 'Offline'),
]

class TeamAdmin(models.Model):


    name = models.CharField(max_length=500, default='name')
    username = models.CharField(max_length=500, default='name')
    email = models.EmailField(unique=True)
    permission = models.CharField(max_length=50, choices=PERMISSION_CHOICES)
    description = models.CharField(max_length=70)
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')
    #new fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    verified = models.BooleanField(default=False)
    cover_image = models.FileField(upload_to='admin_media/', blank=True, null=True)
    profile_image =models.FileField(upload_to="profile_pictures/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

