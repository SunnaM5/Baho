from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from apps.cms.models import (
    SiteSettings,
    HeroSlide,
    HomeSectionLayout,
    ProductCollection,
    FAQItem,
    NewsArticle,
    AdvantageItem
)


@receiver([post_save, post_delete], sender=SiteSettings)
@receiver([post_save, post_delete], sender=HeroSlide)
@receiver([post_save, post_delete], sender=HomeSectionLayout)
@receiver([post_save, post_delete], sender=ProductCollection)
@receiver([post_save, post_delete], sender=FAQItem)
@receiver([post_save, post_delete], sender=NewsArticle)
@receiver([post_save, post_delete], sender=AdvantageItem)
def invalidate_homepage_cache(sender, **kwargs):
    """
    Automatically clear Redis / Django cache when any CMS content changes in Admin.
    """
    for lang in ["ru", "uz", "en"]:
        cache.delete(f"cms_homepage_data_{lang}")
