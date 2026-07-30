from __future__ import annotations

import os
from typing import Dict, Any, List
from django.conf import settings
from apps.products.models import Product
from apps.categories.models import Category
from apps.cms.models import FAQItem


class JsonLdGenerator:
    """
    Generates compliant Schema.org JSON-LD structures for Products, Breadcrumbs, Reviews, Organization, and FAQs.
    """
    SITE_URL = os.getenv("FRONTEND_URL", "https://baho.uz")

    @classmethod
    def get_organization_schema(cls) -> Dict[str, Any]:
        return {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "BAHO-MARKET",
            "url": cls.SITE_URL,
            "logo": f"{cls.SITE_URL}/logo.png",
            "contactPoint": [{
                "@type": "ContactPoint",
                "telephone": "+998712000000",
                "contactType": "customer service",
                "areaServed": "UZ",
                "availableLanguage": ["ru", "uz", "en"]
            }],
            "sameAs": [
                "https://t.me/bahomarket",
                "https://instagram.com/bahomarket"
            ]
        }

    @classmethod
    def get_product_schema(cls, product: Product) -> Dict[str, Any]:
        schema = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": product.name,
            "description": product.description or product.name,
            "sku": product.sku,
            "brand": {
                "@type": "Brand",
                "name": product.brand.name if product.brand else "BAHO"
            },
            "offers": {
                "@type": "Offer",
                "url": f"{cls.SITE_URL}/product/{product.slug}",
                "priceCurrency": "UZS",
                "price": str(product.base_price),
                "availability": "https://schema.org/InStock" if product.stock > 0 else "https://schema.org/OutOfStock",
                "itemCondition": "https://schema.org/NewCondition"
            }
        }

        if hasattr(product, "images") and product.images.exists():
            schema["image"] = [img.image.url for img in product.images.all()]

        if product.rating > 0:
            schema["aggregateRating"] = {
                "@type": "AggregateRating",
                "ratingValue": str(product.rating),
                "reviewCount": str(product.reviews_count or 1)
            }

        return schema

    @classmethod
    def get_breadcrumb_schema(cls, items: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        items format: [{"name": "Home", "url": "/"}, {"name": "Smartphones", "url": "/category/smartphones"}]
        """
        elements = []
        for index, item in enumerate(items, 1):
            elements.append({
                "@type": "ListItem",
                "position": index,
                "name": item["name"],
                "item": f"{cls.SITE_URL}{item['url']}" if not item['url'].startswith("http") else item['url']
            })

        return {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": elements
        }

    @classmethod
    def get_faq_schema(cls, faqs: List[FAQItem]) -> Dict[str, Any]:
        main_entity = []
        for faq in faqs:
            main_entity.append({
                "@type": "Question",
                "name": faq.question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq.answer
                }
            })

        return {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": main_entity
        }


import os
