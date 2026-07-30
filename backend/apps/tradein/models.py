from __future__ import annotations

from django.db import models
from apps.common.models import TimeStampedModel


class TradeInRequest(TimeStampedModel):
    """
    Trade-In evaluation submission model.
    """
    class Condition(models.TextChoices):
        LIKE_NEW = "LIKE_NEW", "Как новый (без царапин)"
        GOOD = "GOOD", "Хорошее (микроцарапины)"
        FAIR = "FAIR", "Удовлетворительное (следы использования)"
        POOR = "POOR", "Плохое (трещины, дефекты)"

    device_name = models.CharField(max_length=255, verbose_name="Модель устройства (например: iPhone 13 Pro)")
    memory_capacity = models.CharField(max_length=50, verbose_name="Объем памяти (например: 128 ГБ)")
    condition = models.CharField(
        max_length=20,
        choices=Condition.choices,
        default=Condition.GOOD,
        verbose_name="Состояние"
    )
    description = models.TextField(blank=True, verbose_name="Описание дефектов / комплектации")
    imei = models.CharField(max_length=50, blank=True, verbose_name="IMEI (необязательно)")
    image = models.ImageField(upload_to="tradein/", blank=True, null=True, verbose_name="Фото устройства")

    customer_name = models.CharField(max_length=150, verbose_name="Имя клиента")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон клиента")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")

    class Meta:
        verbose_name = "Заявка Trade-In"
        verbose_name_plural = "Заявки Trade-In"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Trade-In: {self.device_name} ({self.customer_name})"


class InstallmentPlan(TimeStampedModel):
    """
    Installment tariff configurations (3, 6, 12, 18, 24, 36 months).
    """
    months = models.PositiveIntegerField(unique=True, verbose_name="Срок в месяцах")
    markup_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Процент наценки (например: 15.00 для 15%)",
        verbose_name="Процент наценки"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Тариф рассрочки"
        verbose_name_plural = "Тарифы рассрочки"
        ordering = ["months"]

    def __str__(self) -> str:
        return f"{self.months} месяцев (+{self.markup_percent}%)"
