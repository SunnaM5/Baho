from __future__ import annotations

from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.common.models import TimeStampedModel, SEOFields
from apps.categories.models import Category
from apps.brands.models import Brand


class Product(TimeStampedModel, SEOFields):
    """
    Enterprise Product model supporting multiple images, videos, specs,
    promotions, discounts, ratings, guarantee, inventory stock, and multilingual content.
    """
    name = models.CharField(max_length=255, db_index=True, verbose_name="Название товара (Основное)")
    name_ru = models.CharField(max_length=255, blank=True, db_index=True, verbose_name="Название (RU)")
    name_uz = models.CharField(max_length=255, blank=True, db_index=True, verbose_name="Название (UZ)")
    name_en = models.CharField(max_length=255, blank=True, db_index=True, verbose_name="Название (EN)")

    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL Slug")
    sku = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="Артикул / SKU")
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="products",
        blank=True,
        null=True,
        verbose_name="Бренд"
    )
    
    short_description = models.TextField(blank=True, verbose_name="Краткое описание (Основное)")
    short_description_ru = models.TextField(blank=True, verbose_name="Краткое описание (RU)")
    short_description_uz = models.TextField(blank=True, verbose_name="Краткое описание (UZ)")
    short_description_en = models.TextField(blank=True, verbose_name="Краткое описание (EN)")

    description = models.TextField(blank=True, verbose_name="Полное описание (Основное)")
    description_ru = models.TextField(blank=True, verbose_name="Полное описание (RU)")
    description_uz = models.TextField(blank=True, verbose_name="Полное описание (UZ)")
    description_en = models.TextField(blank=True, verbose_name="Полное описание (EN)")
    
    base_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        blank=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Базовая цена"
    )
    discount_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Цена со скидкой"
    )
    is_on_sale = models.BooleanField(default=False, db_index=True, verbose_name="В акции")

    installment_3m_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Рассрочка на 3 мес. (цена в месяц)",
        help_text="Если не заполнено, будет рассчитано автоматически"
    )
    installment_6m_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Рассрочка на 6 мес. (цена в месяц)",
        help_text="Если не заполнено, будет рассчитано автоматически"
    )
    installment_12m_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Рассрочка на 12 мес. (цена в месяц)",
        help_text="Если не заполнено, будет рассчитано автоматически"
    )
    
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе")
    guarantee_months = models.PositiveIntegerField(default=12, verbose_name="Гарантия (месяцев)")
    battery_health = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Состояние АКБ / Аккумулятора (%)",
        help_text="Опционально. Заполняется для б/у или уцененных смартфонов/гаджетов (например, 85, 92, 100)"
    )
    
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("5.00"))],
        verbose_name="Средний рейтинг"
    )
    reviews_count = models.PositiveIntegerField(default=0, verbose_name="Количество отзывов")
    
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Активен")
    is_featured = models.BooleanField(default=False, db_index=True, verbose_name="Рекомендуемый")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug", "is_active"]),
            models.Index(fields=["sku", "is_active"]),
            models.Index(fields=["is_active", "is_on_sale"]),
            models.Index(fields=["category", "is_active"]),
            models.Index(fields=["brand", "is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.sku})"

    @property
    def current_price(self) -> Decimal:
        if self.is_on_sale and self.discount_price:
            return self.discount_price
        return self.base_price


class ProductColor(TimeStampedModel):
    """
    Color variations for products (e.g. Space Gray, Deep Purple).
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colors")
    name = models.CharField(max_length=50, verbose_name="Цвет (Основное)")
    name_ru = models.CharField(max_length=50, blank=True, verbose_name="Цвет (RU)")
    name_uz = models.CharField(max_length=50, blank=True, verbose_name="Цвет (UZ)")
    name_en = models.CharField(max_length=50, blank=True, verbose_name="Цвет (EN)")
    hex_code = models.CharField(max_length=7, blank=True, help_text="HEX код (#FFFFFF)", verbose_name="HEX код")
    price_override = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Цена для этого цвета (если отличается)",
        help_text="Оставьте пустым, если цена совпадает с базовой"
    )
    image = models.ImageField(
        upload_to="products/colors/",
        blank=True,
        null=True,
        verbose_name="Изображение товара этого цвета"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток данного цвета")

    class Meta:
        verbose_name = "Цвет товара"
        verbose_name_plural = "Цвета товаров"

    def __str__(self) -> str:
        return f"{self.product.name} - {self.name}"


class ProductMemoryVariant(TimeStampedModel):
    """
    Memory/Storage variants (e.g. 128GB, 256GB, 512GB) with price adjustments.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="memory_variants")
    capacity = models.CharField(max_length=50, verbose_name="Объем памяти")
    capacity_ru = models.CharField(max_length=50, blank=True, verbose_name="Память (RU)")
    capacity_uz = models.CharField(max_length=50, blank=True, verbose_name="Память (UZ)")
    capacity_en = models.CharField(max_length=50, blank=True, verbose_name="Память (EN)")
    price_override = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Индивидуальная цена (если отличается)"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток данной модификации")

    class Meta:
        verbose_name = "Вариант памяти"
        verbose_name_plural = "Варианты памяти"

    def __str__(self) -> str:
        return f"{self.product.name} - {self.capacity}"


class ProductSimVariant(TimeStampedModel):
    """
    SIM Card configuration variants (e.g., eSIM, Dual SIM (Physical + eSIM), Dual Physical SIM, Single SIM) with price adjustments.
    """
    SIM_TYPES = [
        ("esim", "eSIM (Только электронная SIM)"),
        ("dual_esim", "Dual SIM (Physical Nano-SIM + eSIM)"),
        ("dual_physical", "Dual Physical SIM (2 Физические nano-SIM, HK/China)"),
        ("single_sim", "Single SIM (1 Физическая SIM)"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sim_variants")
    sim_type = models.CharField(max_length=30, choices=SIM_TYPES, default="dual_esim", verbose_name="Тип SIM-карты")
    name_override = models.CharField(max_length=100, blank=True, verbose_name="Свое название конфигурации (опционально)")
    price_override = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Индивидуальная цена для этой SIM-версии",
        help_text="Оставьте пустым, если цена совпадает с базовой"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток данной SIM-версии")

    class Meta:
        verbose_name = "Вариант SIM-карты"
        verbose_name_plural = "Варианты SIM-карт"

    def __str__(self) -> str:
        return f"{self.product.name} - {self.name_override or self.get_sim_type_display()}"


class ProductVariant(TimeStampedModel):
    """
    Full SKU Combination matrix (e.g. 1TB + Single SIM + Deep Blue = 28,700,000 UZS, 256GB + eSIM + Cosmic Orange = 18,500,000 UZS)
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    memory = models.ForeignKey(ProductMemoryVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name="sku_variants", verbose_name="Память")
    sim = models.ForeignKey(ProductSimVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name="sku_variants", verbose_name="SIM-карта")
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True, blank=True, related_name="sku_variants", verbose_name="Цвет")
    
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Итоговая цена этой комбинации (сум)",
        help_text="Точная цена при выборе этой комбинации памяти, SIM и цвета"
    )
    old_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Старая цена (для скидки)"
    )
    stock = models.PositiveIntegerField(default=1, verbose_name="Остаток данной конкретной комбинации")
    sku = models.CharField(max_length=100, blank=True, verbose_name="Уникальный SKU вариации")
    
    installment_3m_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Рассрочка 3 мес (в мес)",
        help_text="Оставьте пустым для авторасчета от цены этой комбинации"
    )
    installment_6m_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Рассрочка 6 мес (в мес)",
        help_text="Оставьте пустым для авторасчета от цены этой комбинации"
    )
    installment_12m_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Рассрочка 12 мес (в мес)",
        help_text="Оставьте пустым для авторасчета от цены этой комбинации"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "⚡ Точная комбинация товара (Память + SIM + Цвет)"
        verbose_name_plural = "⚡ Точные комбинации цен и остатков (Matrix Pricing)"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "memory", "sim", "color"],
                name="unique_product_memory_sim_color_combination"
            )
        ]

    def __str__(self) -> str:
        mem_str = self.memory.capacity if self.memory else "Любая память"
        sim_str = (self.sim.name_override or self.sim.get_sim_type_display()) if self.sim else "Любая SIM"
        color_str = self.color.name if self.color else "Любой цвет"
        return f"{self.product.name} [{mem_str} | {sim_str} | {color_str}] — {self.price} сум"


class ProductImage(TimeStampedModel):
    """
    Multiple images per product.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True, blank=True, related_name="gallery_images", verbose_name="Привязать к цвету (опционально)")
    image = models.ImageField(upload_to="products/images/", verbose_name="Изображение")
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Alt текст")
    is_main = models.BooleanField(default=False, verbose_name="Главное изображение")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"
        ordering = ["order", "-is_main"]

    def __str__(self) -> str:
        return f"Image for {self.product.name}"


class ProductVideo(TimeStampedModel):
    """
    Multiple video links or uploads per product.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="videos")
    video_url = models.URLField(max_length=500, verbose_name="Ссылка на видео (YouTube / Shorts / MP4)")
    title = models.CharField(max_length=255, blank=True, verbose_name="Заголовок видео")

    class Meta:
        verbose_name = "Видео товара"
        verbose_name_plural = "Видео товаров"

    def __str__(self) -> str:
        return f"Video for {self.product.name}"


class ProductSpecification(TimeStampedModel):
    """
    Key-Value specs for deep searching and filtering (e.g. Screen, Processor, Battery).
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    name = models.CharField(max_length=100, verbose_name="Характеристика")
    name_ru = models.CharField(max_length=100, blank=True, verbose_name="Характеристика (RU)")
    name_uz = models.CharField(max_length=100, blank=True, verbose_name="Характеристика (UZ)")
    name_en = models.CharField(max_length=100, blank=True, verbose_name="Характеристика (EN)")

    value = models.CharField(max_length=255, verbose_name="Значение")
    value_ru = models.CharField(max_length=255, blank=True, verbose_name="Значение (RU)")
    value_uz = models.CharField(max_length=255, blank=True, verbose_name="Значение (UZ)")
    value_en = models.CharField(max_length=255, blank=True, verbose_name="Значение (EN)")

    class Meta:
        verbose_name = "Характеристика товара"
        verbose_name_plural = "Характеристики товаров"

    def __str__(self) -> str:
        return f"{self.product.name} - {self.name}: {self.value}"
