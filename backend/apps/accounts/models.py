from __future__ import annotations

import uuid
from typing import Any
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from apps.common.models import TimeStampedModel

phone_regex = RegexValidator(
    regex=r"^\+998\d{9}$",
    message="Номер телефона должен быть в формате: '+998901234567'."
)


class UserManager(BaseUserManager):
    """
    Custom user manager supporting username or phone number authentication.
    """
    def create_user(self, username: str, password: str | None = None, **extra_fields: Any) -> User:
        if not username:
            raise ValueError("Имя пользователя (username) обязательно")
        username = username.strip()
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, password: str | None = None, **extra_fields: Any) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", User.Role.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser, TimeStampedModel):
    """
    Custom User Model supporting Username and optional Phone Number authentication.
    """
    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Клиент"
        MANAGER = "MANAGER", "Менеджер"
        ADMIN = "ADMIN", "Администратор"

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Имя пользователя (Логин)"
    )
    email = models.EmailField(blank=True, null=True, unique=True, verbose_name="Email")
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        validators=[phone_regex],
        db_index=True,
        verbose_name="Номер телефона"
    )
    first_name = models.CharField(max_length=150, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Фамилия")
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
        verbose_name="Роль"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.username


class UserAddress(TimeStampedModel):
    """
    Saved delivery addresses for a customer.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name="Пользователь"
    )
    title = models.CharField(max_length=100, help_text="Например: Дом, Работа", verbose_name="Название")
    city = models.CharField(max_length=100, default="Ташкент", verbose_name="Город")
    district = models.CharField(max_length=100, blank=True, verbose_name="Район")
    street = models.CharField(max_length=255, verbose_name="Улица")
    building = models.CharField(max_length=50, verbose_name="Дом / Корпус")
    apartment = models.CharField(max_length=50, blank=True, verbose_name="Квартира / Офис")
    floor = models.CharField(max_length=20, blank=True, verbose_name="Этаж")
    comment = models.TextField(blank=True, verbose_name="Комментарий курьеру")
    is_default = models.BooleanField(default=False, verbose_name="По умолчанию")

    class Meta:
        verbose_name = "Адрес доставки"
        verbose_name_plural = "Адреса доставки"
        ordering = ["-is_default", "-created_at"]

    def __str__(self) -> str:
        return f"{self.title}: {self.city}, {self.street} {self.building}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.is_default:
            UserAddress.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
