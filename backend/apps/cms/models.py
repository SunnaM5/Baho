from __future__ import annotations

from django.db import models
from apps.common.models import TimeStampedModel, SEOFields
from apps.products.models import Product


class SiteSettings(TimeStampedModel, SEOFields):
    """
    Global Site Settings (Singleton pattern logic via Admin / API).
    """
    site_name = models.CharField(max_length=255, default="BAHO MARKET", verbose_name="Название сайта")
    logo = models.ImageField(upload_to="cms/site/", blank=True, null=True, verbose_name="Логотип")
    favicon = models.ImageField(upload_to="cms/site/", blank=True, null=True, verbose_name="Favicon")
    
    phone_primary = models.CharField(max_length=50, default="+998 71 200 00 00", verbose_name="Основной телефон")
    phone_secondary = models.CharField(max_length=50, blank=True, default="", verbose_name="Доп. телефон")
    email = models.EmailField(default="info@baho.uz", verbose_name="Email support")
    address = models.CharField(max_length=255, default="Ташкент, Узбекистан", verbose_name="Физический адрес")
    google_maps_url = models.URLField(max_length=500, blank=True, default="", verbose_name="Ссылка Google Maps")
    working_hours = models.CharField(max_length=255, default="Пн-Вс: 09:00 - 21:00", verbose_name="Рабочее время")

    telegram_url = models.URLField(blank=True, default="", verbose_name="Telegram")
    instagram_url = models.URLField(blank=True, default="", verbose_name="Instagram")
    facebook_url = models.URLField(blank=True, default="", verbose_name="Facebook")
    youtube_url = models.URLField(blank=True, default="", verbose_name="YouTube")
    tiktok_url = models.URLField(blank=True, default="", verbose_name="TikTok")

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self) -> str:
        return f"Site Settings: {self.site_name}"


class HeroSlide(TimeStampedModel):
    """
    Slides for main Hero Banner on homepage.
    """
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Заголовок (RU)")
    title_uz = models.CharField(max_length=255, blank=True, verbose_name="Заголовок (UZ)")
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Заголовок (EN)")

    subtitle_ru = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок (RU)")
    subtitle_uz = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок (UZ)")
    subtitle_en = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок (EN)")

    desktop_image = models.ImageField(upload_to="cms/hero/", verbose_name="Баннер для ПК")
    mobile_image = models.ImageField(upload_to="cms/hero/", blank=True, null=True, verbose_name="Баннер для мобильных")

    button_text_ru = models.CharField(max_length=100, blank=True, verbose_name="Текст кнопки (RU)")
    button_text_uz = models.CharField(max_length=100, blank=True, verbose_name="Текст кнопки (UZ)")
    button_text_en = models.CharField(max_length=100, blank=True, verbose_name="Текст кнопки (EN)")
    button_url = models.CharField(max_length=500, blank=True, default="#", verbose_name="Ссылка кнопки")

    bg_color = models.CharField(max_length=30, default="#000000", verbose_name="Цвет фона (HEX)")
    priority = models.PositiveIntegerField(default=0, verbose_name="Приоритет/Порядок")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Слайд главного баннера"
        verbose_name_plural = "Слайды главного баннера"
        ordering = ["priority", "-created_at"]

    def __str__(self) -> str:
        return self.title_ru or "Hero Slide"


from django.utils.text import slugify


class HomeSectionLayout(TimeStampedModel):
    """
    Dynamic ordering & visibility of homepage blocks without code changes.
    """
    SECTION_TYPES = [
        ("hero", "Hero Slider"),
        ("categories", "Категории"),
        ("popular", "Популярные товары"),
        ("tradein", "Блок Trade-In"),
        ("discount", "Товары со скидкой / Акции"),
        ("collections", "Пользовательские подборки"),
        ("advantages", "Преимущества магазина"),
        ("news", "Новости и статьи"),
        ("partners", "Партнеры и Бренды"),
        ("faq", "Часто задаваемые вопросы (FAQ)"),
        ("footer", "Футер и Контакты"),
    ]

    section_key = models.CharField(max_length=50, choices=SECTION_TYPES, unique=True, verbose_name="Ключ секции")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Заголовок блока (RU)")
    title_uz = models.CharField(max_length=255, blank=True, verbose_name="Заголовок блока (UZ)")
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Заголовок блока (EN)")
    order = models.PositiveIntegerField(default=0, unique=True, verbose_name="Порядок вывода")
    is_visible = models.BooleanField(default=True, db_index=True, verbose_name="Отображать блок")

    class Meta:
        verbose_name = "Порядок секций главной страницы"
        verbose_name_plural = "Порядок секций главной страницы"
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.get_section_key_display()} (Order: {self.order})"


class ProductCollection(TimeStampedModel, SEOFields):
    """
    Custom product collections (e.g., 'До 5 млн', 'Популярные', 'Apple Deals').
    """
    title_ru = models.CharField(max_length=255, verbose_name="Название подборки (RU)")
    title_uz = models.CharField(max_length=255, blank=True, verbose_name="Название подборки (UZ)")
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Название подборки (EN)")
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_index=True, verbose_name="URL Slug")
    
    banner_image = models.ImageField(upload_to="cms/collections/", blank=True, null=True, verbose_name="Баннер подборки")
    products = models.ManyToManyField(Product, related_name="collections", blank=True, verbose_name="Товары подборки")
    
    is_featured_on_home = models.BooleanField(default=False, db_index=True, verbose_name="Выводить на главной")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Подборка товаров"
        verbose_name_plural = "Подборки товаров"
        ordering = ["order", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_ru or self.title_en or "collection")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title_ru


class FAQItem(TimeStampedModel):
    """
    Frequently Asked Questions managed from Admin.
    """
    question_ru = models.CharField(max_length=500, verbose_name="Вопрос (RU)")
    question_uz = models.CharField(max_length=500, blank=True, verbose_name="Вопрос (UZ)")
    question_en = models.CharField(max_length=500, blank=True, verbose_name="Вопрос (EN)")

    answer_ru = models.TextField(verbose_name="Ответ (RU)")
    answer_uz = models.TextField(blank=True, verbose_name="Ответ (UZ)")
    answer_en = models.TextField(blank=True, verbose_name="Ответ (EN)")

    category_name = models.CharField(max_length=100, default="Общие вопросы", verbose_name="Категория вопроса")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Вопрос-Ответ (FAQ)"
        verbose_name_plural = "Вопросы-Ответы (FAQ)"
        ordering = ["order", "-created_at"]

    def __str__(self) -> str:
        return self.question_ru


class NewsArticle(TimeStampedModel, SEOFields):
    """
    Enterprise News & Blog CMS entity.
    """
    title_ru = models.CharField(max_length=255, verbose_name="Заголовок (RU)")
    title_uz = models.CharField(max_length=255, blank=True, verbose_name="Заголовок (UZ)")
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Заголовок (EN)")
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_index=True, verbose_name="URL Slug")

    summary_ru = models.TextField(blank=True, verbose_name="Краткое описание (RU)")
    summary_uz = models.TextField(blank=True, verbose_name="Краткое описание (UZ)")
    summary_en = models.TextField(blank=True, verbose_name="Краткое описание (EN)")

    content_ru = models.TextField(verbose_name="Полный текст (RU)")
    content_uz = models.TextField(blank=True, verbose_name="Полный текст (UZ)")
    content_en = models.TextField(blank=True, verbose_name="Полный текст (EN)")

    cover_image = models.ImageField(upload_to="cms/news/", verbose_name="Обложка новости")
    published_at = models.DateTimeField(db_index=True, verbose_name="Дата публикации")
    is_published = models.BooleanField(default=True, db_index=True, verbose_name="Опубликовано")

    class Meta:
        verbose_name = "Новость / Статья"
        verbose_name_plural = "Новости и статьи"
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            generated = slugify(self.title_ru or self.title_en or "article")
            if not generated:
                # Transliteration fallback if django slugify yields empty for non-latin
                import uuid
                generated = f"article-{uuid.uuid4().hex[:8]}"
            self.slug = generated
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title_ru


class AdvantageItem(TimeStampedModel):
    """
    Store advantages (e.g. Быстрая доставка, Гарантия 12 месяцев).
    """
    title_ru = models.CharField(max_length=255, verbose_name="Преимущество (RU)")
    title_uz = models.CharField(max_length=255, blank=True, verbose_name="Преимущество (UZ)")
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Преимущество (EN)")

    subtitle_ru = models.CharField(max_length=255, blank=True, verbose_name="Описание (RU)")
    subtitle_uz = models.CharField(max_length=255, blank=True, verbose_name="Описание (UZ)")
    subtitle_en = models.CharField(max_length=255, blank=True, verbose_name="Описание (EN)")

    icon_name = models.CharField(max_length=100, help_text="Lucide/FontAwesome Icon key", verbose_name="Имя иконки")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Преимущество магазина"
        verbose_name_plural = "Преимущества магазина"
        ordering = ["order"]

    def __str__(self) -> str:
        return self.title_ru
