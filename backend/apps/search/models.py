from __future__ import annotations

from django.db import models
from django.conf import settings
from apps.common.models import TimeStampedModel


class SearchSynonym(TimeStampedModel):
    """
    Search Synonym dictionary managed from Admin.
    Maps terms (e.g. 'айфон', 'эпл', '16про') to target standard search terms ('iphone', 'apple', '16 pro').
    """
    source_term = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="Исходный термин / Синоним")
    target_terms = models.CharField(max_length=255, help_text="Заменяемые ключевые слова через запятую", verbose_name="Целевые термины")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Синоним поиска"
        verbose_name_plural = "Словарь синонимов"

    def __str__(self) -> str:
        return f"{self.source_term} -> {self.target_terms}"


class PopularSearchQuery(TimeStampedModel):
    """
    Popular search query statistics and manually boosted search suggestions.
    """
    query = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="Поисковый запрос")
    search_count = models.PositiveIntegerField(default=1, db_index=True, verbose_name="Количество поисков")
    results_count = models.PositiveIntegerField(default=0, verbose_name="Последнее кол-во результатов")
    is_pinned = models.BooleanField(default=False, db_index=True, verbose_name="Закрепить в рекомендуемых")

    class Meta:
        verbose_name = "Популярный запрос"
        verbose_name_plural = "Популярные запросы"
        ordering = ["-is_pinned", "-search_count"]

    def __str__(self) -> str:
        return f"{self.query} ({self.search_count} поисков)"


class SearchHistory(TimeStampedModel):
    """
    User search history linked to registered User or Guest Session Key.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="search_history")
    session_key = models.CharField(max_length=100, blank=True, db_index=True, verbose_name="Сессия гостя")
    query = models.CharField(max_length=255, verbose_name="Текст запроса")
    results_count = models.PositiveIntegerField(default=0, verbose_name="Найдено товаров")

    class Meta:
        verbose_name = "История поиска"
        verbose_name_plural = "История поиска"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        user_info = self.user.phone if self.user else f"Guest ({self.session_key})"
        return f"{user_info}: {self.query}"


class SearchAnalytics(TimeStampedModel):
    """
    Analytics log for zero-result queries, conversions, and search CTR tracking.
    """
    query = models.CharField(max_length=255, db_index=True, verbose_name="Запрос")
    results_count = models.PositiveIntegerField(default=0, verbose_name="Кол-во результатов")
    clicked_product_id = models.PositiveBigIntegerField(null=True, blank=True, verbose_name="Кликнутый товар ID")
    converted_order = models.BooleanField(default=False, verbose_name="Конверсия в заказ")
    user_agent = models.CharField(max_length=255, blank=True, verbose_name="User Agent")

    class Meta:
        verbose_name = "Аналитика поиска"
        verbose_name_plural = "Аналитика поиска"
        ordering = ["-created_at"]
