from __future__ import annotations

from decimal import Decimal
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from apps.orders.models import Order, OrderItem, OrderHistory
from apps.products.models import Product, ProductVariant
from apps.cart.models import Cart
from apps.telegram.services import send_telegram_message_task


class OrderService:
    """
    Domain Service for atomic order processing, stock locking (select_for_update),
    idempotency key verification, cart cleanup, and asynchronous Telegram alert dispatch via on_commit.
    """
    @staticmethod
    @transaction.atomic
    def create_order(
        full_name: str,
        phone_number: str,
        delivery_address: str,
        items_data: list[dict],
        user=None,
        email: str = "",
        delivery_method: str = Order.DeliveryMethod.COURIER,
        payment_method: str = Order.PaymentMethod.CASH,
        comment: str = "",
        cart_id: str | None = None,
        idempotency_key: str | None = None
    ) -> Order:
        if not items_data:
            raise ValidationError("Невозможно оформить заказ с пустым списком товаров.")

        # Idempotency check: if an order with this key already exists, return it immediately
        if idempotency_key:
            existing_order = Order.objects.filter(idempotency_key=idempotency_key).first()
            if existing_order:
                return existing_order

        try:
            order = Order.objects.create(
                user=user,
                full_name=full_name,
                phone_number=phone_number,
                email=email,
                delivery_method=delivery_method,
                delivery_address=delivery_address,
                payment_method=payment_method,
                comment=comment,
                idempotency_key=idempotency_key
            )
        except IntegrityError:
            # Concurrent duplicate request caught by unique database constraint
            existing_order = Order.objects.filter(idempotency_key=idempotency_key).first()
            if existing_order:
                return existing_order
            raise

        total = Decimal("0.00")
        first_product_image = None

        for item in items_data:
            product_id = item["product_id"]
            variant_id = item.get("variant_id")
            quantity = int(item["quantity"])

            if quantity < 1:
                raise ValidationError("Количество товара должно быть не менее 1.")
            
            # Select for update to handle concurrent checkout & prevent overselling
            try:
                product = Product.objects.select_for_update().get(id=product_id, is_active=True)
            except Product.DoesNotExist:
                raise ValidationError(f"Товар с ID {product_id} не доступен или был удален.")

            variant = None
            if variant_id:
                try:
                    variant = ProductVariant.objects.select_for_update().get(id=variant_id, product=product, is_active=True)
                except ProductVariant.DoesNotExist:
                    raise ValidationError(f"Вариация SKU с ID {variant_id} не найдена.")

            # Calculate source-of-truth unit price
            if variant:
                if variant.stock < quantity:
                    raise ValidationError(f"Недостаточно модификации '{variant.sku}' на складе. В наличии: {variant.stock}")
                unit_price = variant.price
                variant.stock -= quantity
                variant.save(update_fields=["stock"])
            else:
                if product.stock < quantity:
                    raise ValidationError(f"Недостаточно товара '{product.name}' на складе. В наличии: {product.stock}")
                unit_price = product.current_price
                product.stock -= quantity
                product.save(update_fields=["stock"])

            # Check for Price Change mismatch if client expected_price provided
            client_price = item.get("expected_price")
            if client_price is not None and Decimal(str(client_price)) != unit_price:
                raise ValidationError({
                    "code": "PRICE_CHANGED",
                    "product_id": str(product.id),
                    "old_price": str(client_price),
                    "new_price": str(unit_price),
                    "message": f"Цена товара '{product.name}' изменилась с {client_price} на {unit_price} сум."
                })

            color_name = item.get("color_name") or (variant.color.name if variant and variant.color else "")
            memory_capacity = item.get("memory_capacity") or (variant.memory.capacity if variant and variant.memory else "")
            sim_type = variant.sim.get_sim_type_display() if variant and variant.sim else ""
            sku_snapshot = variant.sku if variant else product.sku

            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                variant=variant,
                product_name=product.name,
                color_name=color_name,
                memory_capacity=memory_capacity,
                sim_type=sim_type,
                sku_snapshot=sku_snapshot,
                price=unit_price,
                quantity=quantity
            )

            total += order_item.total_price

            if not first_product_image:
                main_img = product.images.filter(is_main=True).first() or product.images.first()
                if main_img and main_img.image:
                    first_product_image = main_img.image.url

        order.total_amount = total
        order.save(update_fields=["total_amount"])

        OrderHistory.objects.create(
            order=order,
            old_status="",
            new_status=Order.Status.NEW,
            comment="Заказ успешно оформлен"
        )

        # Clear cart if cart_id provided or user authenticated
        if cart_id:
            Cart.objects.filter(id=cart_id).delete()
        elif user and hasattr(user, "cart"):
            user.cart.items.all().delete()

        # Trigger Telegram Bot Alert ONLY AFTER transaction commit
        transaction.on_commit(lambda: OrderService.notify_telegram_new_order(order, first_product_image))

        return order

    @staticmethod
    def notify_telegram_new_order(order: Order, image_url: str | None = None) -> None:
        items_text = ""
        for idx, item in enumerate(order.items.all(), 1):
            details = []
            if item.color_name:
                details.append(item.color_name)
            if item.memory_capacity:
                details.append(item.memory_capacity)
            details_str = f" ({', '.join(details)})" if details else ""
            items_text += f"{idx}. {item.product_name}{details_str} x{item.quantity} - {item.total_price:,.0f} сум\n"

        msg = (
            f"📦 <b>Новый заказ #{order.order_number}</b>\n\n"
            f"<b>Дата:</b> {order.created_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"<b>Клиент:</b> {order.full_name}\n"
            f"<b>Телефон:</b> {order.phone_number}\n"
            f"<b>Доставка:</b> {order.get_delivery_method_display()}\n"
            f"<b>Адрес:</b> {order.delivery_address}\n"
            f"<b>Оплата:</b> {order.get_payment_method_display()}\n"
            f"<b>Комментарий:</b> {order.comment or '—'}\n\n"
            f"<b>Товары:</b>\n{items_text}\n"
            f"💰 <b>Итоговая сумма: {order.total_amount:,.0f} сум</b>"
        )
        send_telegram_message_task.delay(msg, photo_url=image_url)
