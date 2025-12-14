from django.db import models
from django.conf import settings

class FollowRequest(models.Model):
    follow_requester = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requests_sent', on_delete=models.CASCADE)
    requested_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follow_requester', 'requested_user') # Prevent duplicate requests
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follow_requester} wants to follow {self.requested_user}"