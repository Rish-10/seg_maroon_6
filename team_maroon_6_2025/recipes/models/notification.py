from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

class Notification(models.Model):
    """
    Model representing a user notification, for example for follows,
    comments, favourites etc.

    Fields:
        recipient: The user that received the notification.
        sender: The user that instigated the notification.
        notification_type (CharField): The type of notification sent.
        content_type: The content type of the object- used for notification filtering.
        object_id (PositiveIntegerField): The id of the notification in the corresponding content table.
        target_object: The target object that the notification should lead to when clicked.
        created_at (DateTimeField): The date and time the notification was created.
    """

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