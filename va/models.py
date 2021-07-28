from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey


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


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # item = models.ForeignKey(
    #     Cpu, on_delete=models.CASCADE, blank=True, null=True)
    # product = models.ForeignKey(
    #     Gpu, on_delete=models.CASCADE, blank=True, null=True)
    # product2 = models.ForeignKey(
    #     Ram, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.user.first_name


class Cpu(models.Model):
    title = models.CharField(max_length=30)
    specs = models.CharField(max_length=30)
    slug = models.SlugField()
    price = models.FloatField()
    objects = CpuManager()
    orderitem = GenericRelation(
        OrderItem, related_query_name='cpu')

    def __str__(self):
        return self.title


class Gpu(models.Model):
    title = models.CharField(max_length=30)
    specs = models.CharField(max_length=30)
    slug = models.SlugField()
    price = models.FloatField()
    objects = CpuManager()
    orderitem = GenericRelation(
        OrderItem, related_query_name='gpu')

    def __str__(self):
        return self.title


class Ram(models.Model):
    title = models.CharField(max_length=30)
    specs = models.CharField(max_length=30)
    slug = models.SlugField()
    price = models.FloatField()
    objects = CpuManager()
    orderitem = GenericRelation(
        OrderItem, related_query_name='ram')

    def __str__(self):
        return self.title


class Custom(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    cpu = models.ForeignKey(
        Cpu, on_delete=models.SET_NULL, blank=True, null=True)
    gpu = models.ForeignKey(
        Gpu, on_delete=models.SET_NULL, blank=True, null=True)
    ram = models.ForeignKey(
        Ram, on_delete=models.SET_NULL, blank=True, null=True)

    def get_total_item_price(self):
        return self.cpu.price + self.gpu.price + self.ram.price


class Pcdes(models.Model):
    des1 = CharField(max_length=200, null=True, blank=True)
    des2 = CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.des1


class Pcprice(models.Model):
    name = CharField(max_length=500, null=True, blank=True)
    price = models.FloatField()
    qua = models.IntegerField()
    ava = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Pcpart(models.Model):
    name = CharField(max_length=50, null=True, blank=True)
    wifi = models.BooleanField(default=True)
    blutooth = models.BooleanField(default=True)
    vr = models.BooleanField(default=True)
    stream = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Gamingpc(models.Model):
    name = CharField(max_length=100, null=True, blank=True)
    cpu = CharField(max_length=100, null=True, blank=True)
    gpu = CharField(max_length=100, null=True, blank=True)
    ram = CharField(max_length=100, null=True, blank=True)
    des = ForeignKey(Pcdes, on_delete=models.SET_NULL, blank=True, null=True)
    price = ForeignKey(Pcprice, on_delete=models.SET_NULL,
                       blank=True, null=True)
    part = ForeignKey(Pcpart, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name
