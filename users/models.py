from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserProfile(models.Model):
    """
    Extended user profile with additional information
    """
    ROLE_CHOICES = [
        ('student', 'UG Student'),
        ('pg_student', 'PG Student'),
        ('fresher', 'Fresher'),
        ('career_switcher', 'Career Switcher'),
        ('professional', 'Working Professional'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Phone must be 10 digits')],
        unique=True
    )
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    current_experience = models.CharField(max_length=100, blank=True)
    target_role = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class OTPVerification(models.Model):
    """
    OTP verification for phone and email
    """
    OTP_TYPE_CHOICES = [
        ('phone', 'Phone OTP'),
        ('email', 'Email OTP'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    otp = models.CharField(max_length=6)
    otp_type = models.CharField(max_length=10, choices=OTP_TYPE_CHOICES)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.username} - {self.otp_type}"
    
    class Meta:
        ordering = ['-created_at']
