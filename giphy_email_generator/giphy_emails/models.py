from django.db import models

class Email(models.Model):
    recipient = models.EmailField()
    sender = models.EmailField()
    subject = models.TextField()
    message = models.TextField()
    gif_url = models.URLField()
    language = models.CharField(max_length=10)
    sent_at = models.DateTimeField(auto_now_add=True)
