from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class QuerySet(models.QuerySet):
    def search(self, slug=None):
        qs = self
        if slug is not None:
            or_lookup = (Q(title__icontains=slug) |
                         Q(slug__icontains=slug)
                         )
            # distinct() is often necessary with Q lookups
            qs = qs.filter(or_lookup).distinct()
        return qs


class CpuManager(models.Manager):
    def get_queryset(self):
        return QuerySet(self.model, using=self._db)

    def search(self, slug=None):
        return self.get_queryset().search(slug=slug)


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, email, password):
        new = self.create_user(
            first_name=first_name,
            email=email,
            password=password
        )
        new.is_active = True
        new.is_staff = True
        new.is_superuser = True
        new.save(using=self._db)
        return new


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    des = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Cpu(models.Model):
    title = models.CharField(max_length=30)
    specs = models.CharField(max_length=30)
    slug = models.SlugField()
    objects = CpuManager()

    def __str__(self):
        return self.title


class Gpu(models.Model):
    title = models.CharField(max_length=30)
    specs = models.CharField(max_length=30)
    slug = models.SlugField()
    objects = CpuManager()

    def __str__(self):
        return self.title


class Ram(models.Model):
    title = models.CharField(max_length=30)
    specs = models.CharField(max_length=30)
    slug = models.SlugField()
    objects = CpuManager()

    def __str__(self):
        return self.title
