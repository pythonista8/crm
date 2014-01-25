import warnings

from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager,
                                        SiteProfileNotAvailable)


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_superuser, **extra_fields):
        """Creates and saves a User with the given email and password."""
        now = timezone.now()
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_created=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, **extra_fields)


class Company(models.Model):
    """Foreign keys: `users`."""
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    postcode = models.PositiveIntegerField(blank=True, null=True)

    # Date Records.
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    """Foreign keys: `customers`, `meetings`, `followups`."""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    # Subscription Plan Info.
    TRIAL = 'trial'
    INDIVIDUAL = 'individual'
    COMPANY = 'company'
    ENTERPRISE = 'enterprise'
    SUBSCRIPTION_PLAN_CHOICES = (
        (TRIAL, "Free Trial"),
        (INDIVIDUAL, "Individual"),
        (COMPANY, "Company"),
        (ENTERPRISE, "Enterprise"),
    )

    subscription_plan = models.CharField(
        max_length=100, choices=SUBSCRIPTION_PLAN_CHOICES, default=TRIAL)

    # Company Info.
    company = models.ForeignKey(Company, related_name='users')
    is_head = models.BooleanField(default=False)

    # Date Records.
    date_created = models.DateTimeField(auto_now_add=True)

    # Managers.
    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_absolute_url(self):
        return "/users/%s/" % self.pk

    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in
        between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user. If a first name is not
        given, return email nickname."""
        if self.first_name:
            return self.first_name
        return self.email[:self.email.find('@')]

    def email_user(self, subject, message, from_email=None):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email])

    @property
    def is_trial(self):
        if self.subscription_plan == self.TRIAL:
            return True
        return False
