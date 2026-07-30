from __future__ import annotations

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.cart.models import Cart, CartItem
from apps.cart.serializers import CartSerializer, CartItemSerializer
from apps.cart.services import CartService


class CartViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = CartSerializer

    def get_cart(self) -> Cart:
        return CartService.get_or_create_cart(self.request)

    def list(self, request):
        cart = self.get_cart()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="items")
    def add_item(self, request):
        cart = self.get_cart()
        product_id = request.data.get("product_id")
        variant_id = request.data.get("variant_id")
        quantity = int(request.data.get("quantity", 1))
        color_id = request.data.get("color_id")
        memory_variant_id = request.data.get("memory_variant_id")

        item = CartService.add_to_cart(
            cart=cart,
            product_id=product_id,
            quantity=quantity,
            variant_id=variant_id,
            color_id=color_id,
            memory_variant_id=memory_variant_id
        )
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["patch"], url_path=r"items/(?P<item_id>[^/.]+)")
    def update_item(self, request, item_id=None):
        cart = self.get_cart()
        try:
            item = cart.items.get(id=item_id)
        except CartItem.DoesNotExist:
            return Response({"detail": "Элемент корзины не найден."}, status=status.HTTP_404_NOT_FOUND)

        quantity = int(request.data.get("quantity", item.quantity))
        if quantity < 1:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if item.product.stock < quantity:
            return Response(
                {"detail": f"Недостаточно товара на складе. Доступно: {item.product.stock}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item.quantity = quantity
        item.save(update_fields=["quantity"])
        return Response(CartItemSerializer(item).data)

    @action(detail=False, methods=["delete"], url_path=r"items/(?P<item_id>[^/.]+)")
    def delete_item(self, request, item_id=None):
        cart = self.get_cart()
        try:
            item = cart.items.get(id=item_id)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"detail": "Элемент корзины не найден."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["delete"], url_path="clear")
    def clear(self, request):
        cart = self.get_cart()
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
