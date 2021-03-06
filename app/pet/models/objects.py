import time
from random import randint

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from . import enums
from ..photo_service import upload_photo


class UserManager(BaseUserManager):
    """Custom user manager"""
    def create_user(self, email, nickname, password, **extra_fields):
        if not email or not nickname:
            raise ValueError("All fields are required.")
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, nickname, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, nickname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь с email вместо username"""

    email = models.EmailField(
        "Адрес электронной почты",
        unique=True,
        db_index=True,
    )
    nickname = models.CharField("Никнейм", max_length=64)
    is_staff = models.BooleanField("Статус персонала", default=False)
    is_superuser = models.BooleanField("Статус суперпользователя",
                                       default=False)
    is_active = models.BooleanField("Активирован", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("nickname", )

    objects = UserManager()

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class AnnouncementManager(models.Manager):
    pass


class Announcement(models.Model):
    """Объявление о пропавшем или найденном питомце"""

    ANNOUNCEMENT_TYPES = enums.AnnouncementType.choices
    ANIMAL_TYPES = enums.AnimalType.choices

    user = models.ForeignKey(
        User,
        models.CASCADE,
        "announcements",
        verbose_name="Пользователь",
    )
    description = models.CharField("Описание", max_length=5000)
    photo = models.ImageField("Фотография животного", upload_to=upload_photo)
    announcement_type = models.IntegerField("Тип объявления",
                                            choices=ANNOUNCEMENT_TYPES)
    animal_type = models.IntegerField("Тип животного", choices=ANIMAL_TYPES)
    address = models.CharField("Место пропажи или находки", max_length=1000)
    latitude = models.FloatField("Широта")
    longitude = models.FloatField("Долгота")
    contact_phone_number = models.CharField("Контактный телефон",
                                            max_length=12)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    objects = AnnouncementManager()

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return str(self.user)


def generate_password_reset_confirmation_code():
    """Возвращает случайный (заданной в настройках длины) код"""
    code = randint(
        10**(settings.PASSWORD_RESET_CONFIRMATION_CODE_LENGTH - 1),
        (10**settings.PASSWORD_RESET_CONFIRMATION_CODE_LENGTH) - 1,
    )
    return code


def get_expired_in_time():
    """Возвращает время устаревания кода в секундах"""
    seconds = round(
        time.time()) + settings.PASSWORD_RESET_CONFIRMATION_CODE_LIFE_TIME
    return seconds


class PasswordResetConfirmationCodeManager(models.Manager):
    pass


class PasswordResetConfirmationCode(models.Model):
    """Код подтверждения сброса пароля"""

    user = models.ForeignKey(
        User,
        models.CASCADE,
        "password_reset_codes",
        verbose_name="Пользователь, которому принадлежит этот код",
    )
    code = models.IntegerField(
        "Код подтвержения",
        default=generate_password_reset_confirmation_code,
    )
    expired_in = models.BigIntegerField(
        "Время устаревания кода",
        default=get_expired_in_time,
    )

    objects = PasswordResetConfirmationCodeManager()

    class Meta:
        verbose_name = "Код подтверждения сброса пароля"
        verbose_name_plural = "Коды подтверждения сброса пароля"

    def __str__(self):
        return "{}_{}".format(self.user, self.code)


class SettingsManager(models.Manager):
    def get_actual(self):
        try:
            return self.get_queryset().get(
                settings_name=settings.SETTINGS_ACTUAL_NAME)
        except models.ObjectDoesNotExist:
            return None


class Settings(models.Model):
    """Настройки приложения"""

    settings_name = models.CharField(
        "Уникальное название настроек",
        max_length=200,
        unique=True,
    )
    actual_app_version_ios = models.CharField(
        "Актуальная версия приложения для ios",
        max_length=200,
        blank=True,
        null=True,
    )
    min_app_version_ios = models.CharField(
        "Минимальная версия приложения для ios",
        max_length=200,
        blank=True,
        null=True,
    )

    objects = SettingsManager()

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"

    def __str__(self):
        return self.settings_name
