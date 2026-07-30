from __future__ import annotations

from rest_framework import serializers
from apps.products.models import (
    Product,
    ProductColor,
    ProductMemoryVariant,
    ProductSimVariant,
    ProductVariant,
    ProductImage,
    ProductVideo,
    ProductSpecification
)
from apps.categories.serializers import CategorySerializer
from apps.brands.serializers import BrandSerializer


from apps.common.serializers import TranslatableModelSerializer


class ProductColorSerializer(TranslatableModelSerializer):
    translatable_fields = ("name",)

    class Meta:
        model = ProductColor
        fields = ("id", "name", "hex_code", "image", "price_override", "stock")


class ProductMemoryVariantSerializer(TranslatableModelSerializer):
    translatable_fields = ("capacity",)

    class Meta:
        model = ProductMemoryVariant
        fields = ("id", "capacity", "price_override", "stock")


class ProductSimVariantSerializer(serializers.ModelSerializer):
    sim_type_display = serializers.CharField(source="get_sim_type_display", read_only=True)

    class Meta:
        model = ProductSimVariant
        fields = ("id", "sim_type", "sim_type_display", "name_override", "price_override", "stock")


class ProductVariantSerializer(serializers.ModelSerializer):
    memory_id = serializers.PrimaryKeyRelatedField(source="memory", read_only=True)
    sim_id = serializers.PrimaryKeyRelatedField(source="sim", read_only=True)
    color_id = serializers.PrimaryKeyRelatedField(source="color", read_only=True)
    
    storage = serializers.CharField(source="memory.capacity", read_only=True, default=None)
    sim_type = serializers.CharField(source="sim.get_sim_type_display", read_only=True, default=None)
    color_name = serializers.CharField(source="color.name", read_only=True, default=None)
    color_hex = serializers.CharField(source="color.hex_code", read_only=True, default=None)
    available = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = (
            "id", "sku", "memory_id", "sim_id", "color_id",
            "storage", "sim_type", "color_name", "color_hex",
            "price", "old_price", "installment_3m_price", "installment_6m_price", "installment_12m_price",
            "stock", "is_active", "available"
        )

    def get_available(self, obj: ProductVariant) -> bool:
        return obj.is_active and obj.stock > 0


class ProductImageSerializer(serializers.ModelSerializer):
    color_id = serializers.PrimaryKeyRelatedField(source="color", read_only=True)

    class Meta:
        model = ProductImage
        fields = ("id", "image", "color_id", "alt_text", "is_main", "order")


class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = ("id", "video_url", "title")


class ProductSpecificationSerializer(TranslatableModelSerializer):
    translatable_fields = ("name", "value")

    class Meta:
        model = ProductSpecification
        fields = ("id", "name", "value")


class ProductListSerializer(TranslatableModelSerializer):
    translatable_fields = ("name",)
    category = serializers.CharField(source="category.name", read_only=True)
    brand = serializers.CharField(source="brand.name", read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "sku", "category", "brand",
            "base_price", "discount_price", "current_price",
            "installment_3m_price", "installment_6m_price", "installment_12m_price",
            "is_on_sale", "stock", "battery_health", "rating", "reviews_count",
            "main_image", "is_active", "is_featured"
        )

    def get_main_image(self, obj: Product) -> str | None:
        main = obj.images.filter(is_main=True).first() or obj.images.first()
        if main and main.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(main.image.url)
            return main.image.url
        return None


class ProductDetailSerializer(TranslatableModelSerializer):
    translatable_fields = ("name", "short_description", "description", "meta_title", "meta_description")
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    memory_variants = ProductMemoryVariantSerializer(many=True, read_only=True)
    sim_variants = ProductSimVariantSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    videos = ProductVideoSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "sku", "category", "brand",
            "short_description", "description", "base_price", "discount_price",
            "current_price", "installment_3m_price", "installment_6m_price", "installment_12m_price",
            "is_on_sale", "stock", "guarantee_months", "battery_health",
            "rating", "reviews_count", "colors", "memory_variants", "sim_variants", "variants",
            "images", "videos", "specifications", "is_active", "is_featured",
            "meta_title", "meta_description", "og_title", "og_description", "canonical_url"
        )
