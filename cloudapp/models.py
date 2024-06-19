from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify


class Design(models.Model):
    title = models.CharField(max_length=128, blank=False, null=False, verbose_name='Название')
    file = models.FileField(upload_to='files/design/', max_length=256)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=64, blank=False, null=False, unique=True, verbose_name='Имя пользователя')
    name = models.CharField(max_length=256, blank=False, null=True, verbose_name='Имя')
    surname = models.CharField(max_length=256, blank=False, null=True, verbose_name='Имя')
    patronymic = models.CharField(max_length=256, blank=True, null=True, verbose_name='Имя')
    email = models.EmailField(blank=False, null=True, unique=True, verbose_name='Электронная почта')
    role = models.IntegerField(blank=True, null=True, verbose_name='Роль')
    design_id = models.ForeignKey(Design, models.CASCADE, null=True, verbose_name='Дизайн')
    date_of_register = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    date_of_change = models.DateTimeField(auto_now=True, verbose_name='Дата изменении')
    ban_start = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала блокировки')
    ban_end = models.DateTimeField(blank=True, null=True, verbose_name='Дата конца блокировки')
    subscribe = models.BooleanField(default=0, blank=True, null=True, verbose_name='Подписка')
    is_custom_user = models.BooleanField(default=0)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)


class Image(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False, verbose_name='Название')
    image = models.ImageField(upload_to='users_images/%Y/%m/%d/', blank=False, null=False)
    file_size = models.IntegerField(blank=False, null=False, verbose_name='Размер изображения')
    format = models.CharField(max_length=6, blank=True, null=True, verbose_name='Формат изображения')
    width = models.IntegerField(blank=True, null=False, verbose_name='Ширина')
    height = models.IntegerField(blank=True, null=False, verbose_name='Высота')
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    # archive_id = models.ForeignKey(Archive, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Архив')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    changed_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def get_size(self):
        size = self.file_size
        name = 'б'
        result = 0
        if (size > 1024):
            result = size / 1024
            name = 'Кб'
            if (result > 1024):
                result = result / 1024
                name = 'Мб'
                if (result > 1024):
                    result = result / 1024
                    name = 'Гб'
        return f'{round(result, 2)} {name}'

            # remains = size % 1024
            # remains = round(float('0.' + str(remains)), 2)

class Archive(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False, default='Архив', verbose_name='Название')
    color = models.CharField(max_length=8, blank=True, null=False, default='ffffff', verbose_name='Цвет')
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    images = models.ManyToManyField(Image, verbose_name='Изображения')