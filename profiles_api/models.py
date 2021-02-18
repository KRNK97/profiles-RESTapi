from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

# custom manager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    # we need to define funcs that CLI uses to manage models

    def create_user(self, email, name, password=None):
        """Create new user profile"""
        if not email:
            raise ValueError('User must have email')

        # lower case the 2nd half of email for convenience
        email = self.normalize_email(email)
        # create user model with data given
        user = self.model(email=email, name=name)
        # set password this way as its encrypted
        user.set_password(password)
        # save model
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save new super user"""
        user = self.create_user(email, name, password)

        # assign is superuser
        user.is_staff = True
        user.is_superuser = True    # autocreated from permissions mixin
        user.save(using=self._db)

        return user


# we will customize the standard user model
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """db model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # user profile manager to help in django CLI
    # by default user is created with username field
    # but we used email instead so we need to tell django how to interact with this change and use email as the default field instead of username
    objects = UserProfileManager()

    # user email as USERNAME field
    USERNAME_FIELD = 'email'
    # use name field as well that we created above (extra)
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """get fullname of user"""
        return self.name

    def get_short_name(self):
        """get shortname of user"""
        return self.name

    def __str__(self):
        """return string repr of user"""
        return self.email


class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status_text
