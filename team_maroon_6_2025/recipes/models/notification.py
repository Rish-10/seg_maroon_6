from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

# Model representing a user notification (follow, comment, favourite, etc.)
class Notification(models.Model):
    TYPES = [
        ('favourite', 'New Favourite'),
        ('comment', 'New Comment'),
        ('follow', 'New Follower'),
        ('request', 'Follow Request'),
    ]

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=TYPES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    # Return a readable description of the notification
    def __str__(self):
        return f"{self.sender} -> {self.recipient} ({self.notification_type})"