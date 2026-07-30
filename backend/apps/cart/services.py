from __future__ import annotations

from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.cart.models import Cart, CartItem
from apps.products.models import Product, ProductColor, ProductMemoryVariant, ProductVariant


class CartService:
    """
    Domain Service for cart manipulation, guest merging, and stock checks.
    """
    @staticmethod
    def get_or_create_cart(request) -> Cart:
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            return cart
        
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
        return cart

    @staticmethod
    @transaction.atomic
    def add_to_cart(
        cart: Cart,
        product_id: str,
        quantity: int = 1,
        variant_id: str | None = None,
        color_id: str | None = None,
        memory_variant_id: str | None = None
    ) -> CartItem:
        if quantity < 1:
            raise ValidationError("Количество товара должно быть не менее 1.")

        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            raise ValidationError("Товар не найден или недоступен.")

        variant = None
        if variant_id:
            try:
                variant = ProductVariant.objects.get(id=variant_id, product=product, is_active=True)
                if variant.stock < quantity:
                    raise ValidationError(f"Недостаточно модификации SKU '{variant.sku}' на складе. В наличии: {variant.stock}")
            except ProductVariant.DoesNotExist:
                raise ValidationError("Указанная вариация SKU не найдена.")

        if not variant and product.stock < quantity:
            raise ValidationError(f"Недостаточно товара '{product.name}' на складе. В наличии: {product.stock}")

        color = None
        if color_id:
            try:
                color = ProductColor.objects.get(id=color_id, product=product)
            except ProductColor.DoesNotExist:
                raise ValidationError("Указанный цвет недоступен для этого товара.")

        memory_variant = None
        if memory_variant_id:
            try:
                memory_variant = ProductMemoryVariant.objects.get(id=memory_variant_id, product=product)
            except ProductMemoryVariant.DoesNotExist:
                raise ValidationError("Указанный вариант памяти недоступен для этого товара.")

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            color=color,
            memory_variant=memory_variant,
            defaults={"quantity": quantity}
        )

        if not created:
            new_qty = item.quantity + quantity
            available_stock = variant.stock if variant else product.stock
            if available_stock < new_qty:
                raise ValidationError(f"Невозможно добавить {quantity} шт. На складе всего {available_stock} шт., уже в корзине: {item.quantity} шт.")
            item.quantity = new_qty
            item.save(update_fields=["quantity"])

        return item

    @staticmethod
    @transaction.atomic
    def merge_guest_cart(user, session_key: str | None) -> Cart:
        user_cart, _ = Cart.objects.get_or_create(user=user)
        if not session_key:
            return user_cart

        try:
            guest_cart = Cart.objects.get(session_key=session_key)
        except Cart.DoesNotExist:
            return user_cart

        for item in guest_cart.items.all():
            target_item = user_cart.items.filter(
                product=item.product,
                color=item.color,
                memory_variant=item.memory_variant
            ).first()

            if target_item:
                target_item.quantity += item.quantity
                target_item.save(update_fields=["quantity"])
            else:
                item.cart = user_cart
                item.save(update_fields=["cart"])

        guest_cart.delete()
        return user_cart
