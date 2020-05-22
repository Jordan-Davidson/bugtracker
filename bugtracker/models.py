from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    pass

class Ticket(models.Model):
    title = models.CharField(max_length=30)
    time = models.DateTimeField(default=timezone.now)
    description = models.TextField()

    submitted_by = models.ForeignKey(CustomUser, 
    on_delete=models.CASCADE, 
    related_name='submitted_by')
    choices = (
        ('new', 'new'),
        ('in_progress', 'in progress'),
        ('done', 'done'),
        ('invalid', 'invalid')
    )
    status = models.CharField(max_length = 11, choices=choices, default='new')

    assigned_user = models.ForeignKey(CustomUser,
    on_delete= models.CASCADE,
    default=None,
    related_name='assigned_user',
    null=True)

    completed_by = models.ForeignKey(CustomUser, 
    on_delete=models.CASCADE, 
    default=None,
    related_name='completed_by',
    null=True)
    