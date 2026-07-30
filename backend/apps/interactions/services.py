from __future__ import annotations

import logging
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from apps.interactions.models import StockNotificationRequest

logger = logging.getLogger(__name__)


def process_stock_notifications(product, batch_size: int = 100) -> int:
    """
    Triggers dispatch of stock arrival notifications when product.stock returns > 0.
    Executes in batch chunks with bulk updates for high concurrency and scale.
    """
    if product.stock <= 0:
        return 0

    pending_ids = list(StockNotificationRequest.objects.filter(
        product=product,
        is_notified=False
    ).values_list("id", flat=True))

    if not pending_ids:
        return 0

    dispatched_count = 0

    # Process in batches of size batch_size (default 100)
    for i in range(0, len(pending_ids), batch_size):
        chunk_ids = pending_ids[i:i + batch_size]
        
        with transaction.atomic():
            requests_chunk = list(StockNotificationRequest.objects.filter(
                id__in=chunk_ids,
                is_notified=False
            ).select_for_update().select_related("user"))

            if not requests_chunk:
                continue

            for req in requests_chunk:
                recipient_email = req.email or (req.user.email if req.user and req.user.email else None)
                
                if recipient_email:
                    try:
                        send_mail(
                            subject=f"Товар {product.name} снова в наличии!",
                            message=f"Здравствуйте! Товар '{product.name}' снова доступен для заказа на BAHO-MARKET по цене {product.base_price} сум.",
                            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else "noreply@baho.uz",
                            recipient_list=[recipient_email],
                            fail_silently=True,
                        )
                    except Exception as e:
                        logger.error(f"Failed to send stock notification email to {recipient_email}: {e}")

                req.is_notified = True

            StockNotificationRequest.objects.bulk_update(requests_chunk, ["is_notified"])
            dispatched_count += len(requests_chunk)

    return dispatched_count
