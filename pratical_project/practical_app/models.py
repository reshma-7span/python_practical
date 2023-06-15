from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
# from __future__ import unicode_literals
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from datetime import date
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, name, email,device_token, password=None):
        """
        Creates and saves a User with the given email, mobile, gender and password.
        """
        user = ""
        if not email:
            raise ValueError('Users must have an email address')

        if  name != "manual":
            user = self.model(
                email=self.normalize_email(email),
                name=name,
               device_token=device_token,

            )
        else:
            user = self.model(
                email=self.normalize_email(email),
                name=name,
                device_token=device_token,
                password=password
            )
        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, device_token, password):
        """
        Creates and saves a superuser with the given email, mobile, gender and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            name=name,
            device_token=device_token,

        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)

    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )



    device_token = models.CharField(max_length=5000, default='', blank=True, null=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'device_token']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin






class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    # Add other relevant fields here

    def __str__(self):
        return self.title


class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Add other relevant fields here

    def __str__(self):
        return f"Like {self.like_id} by {self.user} on Post {self.post}"