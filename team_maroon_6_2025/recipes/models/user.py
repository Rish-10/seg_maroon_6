from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar


def validate_bio_lines(value):
    """Refuse input if it has more than 8 lines."""
    if len(value.splitlines()) > 8:
        raise ValidationError("Bio cannot exceed 8 lines.")

class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    favourites = models.ManyToManyField('recipes.Recipe', related_name='favourited_by', blank=True)
    bio = models.TextField(
        max_length=300,
        blank=True,
        validators=[validate_bio_lines]
    )
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)
    is_private = models.BooleanField(
        default=False,
        help_text="Your recipes will only be visible to followers. Other Recipify users will only be able to follow you once you approve their follow request.")


    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        
        return self.gravatar(size=60)

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

class FollowRequest(models.Model):
    follow_requester = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requests_sent', on_delete=models.CASCADE)
    requested_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follow_requester', 'requested_user') # Prevent duplicate requests
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follow_requester} wants to follow {self.requested_user}"