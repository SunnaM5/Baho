from __future__ import annotations

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.tradein.models import TradeInRequest, InstallmentPlan
from apps.telegram.services import send_telegram_message_task

ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB


class TradeInRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeInRequest
        fields = (
            "id", "device_name", "memory_capacity", "condition",
            "description", "imei", "image", "customer_name",
            "phone_number", "comment", "is_processed", "created_at"
        )
        read_only_fields = ("id", "is_processed", "created_at")

    def validate_image(self, value):
        if value:
            ext = value.name.split(".")[-1].lower()
            if ext not in ALLOWED_IMAGE_EXTENSIONS:
                raise ValidationError(f"Неподдерживаемый формат файла. Разрешены: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}")
            if value.size > MAX_FILE_SIZE_BYTES:
                raise ValidationError("Максимальный размер загружаемого изображения — 5 МБ.")

            # Perform strict Pillow magic header binary inspection
            try:
                from PIL import Image
                img = Image.open(value)
                img.verify()
                if img.format.lower() not in ["jpeg", "jpg", "png", "webp"]:
                    raise ValidationError("Содержимое файла не является допустимым изображением (JPEG/PNG/WEBP).")
            except Exception:
                raise ValidationError("Загруженный файл поврежден или не является валидным изображением.")

        return value

    def create(self, validated_data: dict) -> TradeInRequest:
        instance = super().create(validated_data)
        
        msg = (
            f"🔄 <b>Новая заявка Trade-In</b>\n\n"
            f"<b>Устройство:</b> {instance.device_name} ({instance.memory_capacity})\n"
            f"<b>Состояние:</b> {instance.get_condition_display()}\n"
            f"<b>IMEI:</b> {instance.imei or '—'}\n"
            f"<b>Клиент:</b> {instance.customer_name}\n"
            f"<b>Телефон:</b> {instance.phone_number}\n"
            f"<b>Описание:</b> {instance.description or '—'}\n"
            f"<b>Комментарий:</b> {instance.comment or '—'}"
        )
        
        request = self.context.get("request")
        image_url = None
        if instance.image and request:
            image_url = request.build_absolute_uri(instance.image.url)

        send_telegram_message_task.delay(msg, photo_url=image_url)
        return instance


class InstallmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentPlan
        fields = ("id", "months", "markup_percent", "is_active")
