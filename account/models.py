from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from recruit.models import JobOpening


class UserManager(BaseUserManager):
    
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("username은 필수 영역입니다.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
            
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()

    email = None
    applyed = models.ManyToManyField(JobOpening)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    class Meta:
        app_label = 'account'