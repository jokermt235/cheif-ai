import jwt
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from storage.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta


class User(AbstractUser):
  email = models.EmailField(_("email address"), unique=True,db_index=True)
  username = None
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ()
  first_name = models.CharField(_("first name"), max_length=150)
  last_name = models.CharField(_("last name"), max_length=150)
  phone_number = models.CharField(_("phone number"), max_length=70)
  password = models.CharField(_("first name"), max_length=150)
  is_staff = models.BooleanField(
    _("staff status"),
    default=True,
    help_text=_("Designates whether the user can log into this admin site."),
  )
  objects = CustomUserManager()

  @property
  def token(self):
    return self._generate_jwt_token()

  @property
  def refresh(self):
    return self._generate_jwt_token(days=30)

  def _generate_jwt_token(self, days=1):
    dt = datetime.now() + timedelta(days=days)
    token = jwt.encode({
      'id': self.pk,
      'exp': int(dt.strftime('%s'))
      }, settings.SECRET_KEY, algorithm='HS256')
    return token
