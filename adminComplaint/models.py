from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password = None):
        """
            Creates and saves user with the given email, date_of_birth and password
        """
        
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email = self.normalize_email(email), 
        date_of_birth = date_of_birth)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, dob, and password
        """
        user = self.create_user(email, password=password, date_of_birth=date_of_birth)
        user.is_admin = True
        user.save(using = self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name = 'email address', max_length = 255, unique = True,)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin