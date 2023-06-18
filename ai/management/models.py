from distutils.text_file import TextFile
from re import U
import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


# class BaseModel(models.Model):
#     uid=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4())
#     created_at=models.DateTimeField(auto_created=True)
#     updated_at=models.DateTimeField(auto_now_add=True)




#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name,  password=None, password2=None):
      """
      Creates and saves a User with the given email, name, password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
        
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name,  password=None):
      """
      Creates and saves a superuser with the given email, name, password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name']

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


class Products(models.Model):
    name=models.CharField(max_length=255,unique=True)
    description=models.TextField(null=True)
    price=models.IntegerField(default=1)
    status=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
