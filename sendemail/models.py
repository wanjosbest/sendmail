from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    company_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Audience(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="audiences")
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=30,default="general_audience",null=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"


class Subscriber(models.Model):
  
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE, related_name="subscribers", default=85)
    email = models.EmailField(null=True)
    name = models.CharField(max_length=255, blank=True)
    subscribed = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.email} ({'Subscribed' if self.subscribed else 'Unsubscribed'})"

class NewsletterSubscriber(models.Model):

    email = models.EmailField(null=True)
    name = models.CharField(max_length=255, blank=True)
    subscribed = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.email} ({'Subscribed' if self.subscribed else 'Unsubscribed'})"


class EmailTemplate(models.Model):
 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="email_templates")
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body_html = models.TextField()
    body_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Campaign(models.Model):
  
    STATUS_CHOICES = [
        ('draft', 'draft'),
        ('scheduled', 'scheduled'),
        ('sent', 'sent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="campaigns")
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE, related_name="campaigns")
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=255)
    body_html = models.TextField(blank=True, null=True)
    body_text = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    checks = models.BooleanField(default=False)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    sent_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.get_status_display()}"


class EmailLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="email_logs", null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="email_logs")
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='pending')  # pending, sent, bounced, opened, clicked
    sent_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.subscriber.email} - {self.status} ({self.campaign.subject})"


