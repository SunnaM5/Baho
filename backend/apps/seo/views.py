from __future__ import annotations

import os
from django.http import HttpResponse, Http404
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404

from apps.products.models import Product
from apps.categories.models import Category
from apps.cms.models import NewsArticle, FAQItem
from apps.seo.services import JsonLdGenerator


class RobotsTxtView(View):
    """
    GET /robots.txt
    Dynamic robots.txt generator.
    """
    def get(self, request, *args, **kwargs):
        domain = os.getenv("FRONTEND_URL", "https://baho.uz")
        content = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /checkout/
Disallow: /cart/
Disallow: /profile/

Sitemap: {domain}/sitemap.xml
"""
        return HttpResponse(content.strip(), content_type="text/plain")


class DynamicSitemapXmlView(View):
    """
    GET /sitemap.xml
    Dynamic multi-lingual sitemap generator for products, categories, news articles, and core pages.
    """
    def get(self, request, *args, **kwargs):
        domain = os.getenv("FRONTEND_URL", "https://baho.uz")
        urls = [
            f"<url><loc>{domain}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>",
            f"<url><loc>{domain}/catalog</loc><changefreq>daily</changefreq><priority>0.9</priority></url>",
        ]

        # Categories
        for cat in Category.objects.filter(is_active=True).only("slug", "updated_at"):
            urls.append(f"""<url>
                <loc>{domain}/category/{cat.slug}</loc>
                <xhtml:link rel="alternate" hreflang="ru" href="{domain}/ru/category/{cat.slug}"/>
                <xhtml:link rel="alternate" hreflang="uz" href="{domain}/uz/category/{cat.slug}"/>
                <xhtml:link rel="alternate" hreflang="en" href="{domain}/en/category/{cat.slug}"/>
                <priority>0.8</priority>
            </url>""")

        # Products
        for prod in Product.objects.filter(is_active=True).only("slug", "updated_at"):
            urls.append(f"""<url>
                <loc>{domain}/product/{prod.slug}</loc>
                <xhtml:link rel="alternate" hreflang="ru" href="{domain}/ru/product/{prod.slug}"/>
                <xhtml:link rel="alternate" hreflang="uz" href="{domain}/uz/product/{prod.slug}"/>
                <xhtml:link rel="alternate" hreflang="en" href="{domain}/en/product/{prod.slug}"/>
                <priority>0.9</priority>
            </url>""")

        # News Articles
        for article in NewsArticle.objects.filter(is_published=True).only("slug", "updated_at"):
            urls.append(f"""<url>
                <loc>{domain}/news/{article.slug}</loc>
                <priority>0.6</priority>
            </url>""")

        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
{"".join(urls)}
</urlset>"""

        return HttpResponse(xml_content.strip(), content_type="application/xml")


class SeoMetaView(APIView):
    """
    GET /api/v1/seo/meta/?entity_type=product&slug=iphone-16-pro
    Returns canonical, hreflang mappings, OpenGraph, Twitter Cards, and JSON-LD structured data.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        entity_type = request.query_params.get("entity_type", "home")
        slug = request.query_params.get("slug")
        domain = os.getenv("FRONTEND_URL", "https://baho.uz")

        meta = {
            "title": "BAHO-MARKET — Интернет-магазин электроники и техники",
            "description": "Широкий ассортимент смартфонов, гаджетов и бытовой техники в Ташкенте и Узбекистане.",
            "canonical": f"{domain}/",
            "og_title": "BAHO-MARKET — Интернет-магазин",
            "og_description": "Быстрая доставка, гарантия качества, выгодные рассрочки.",
            "og_image": f"{domain}/og-default.jpg",
            "twitter_card": "summary_large_image",
            "hreflang": {
                "ru": f"{domain}/ru/",
                "uz": f"{domain}/uz/",
                "en": f"{domain}/en/",
            },
            "json_ld": [JsonLdGenerator.get_organization_schema()]
        }

        if entity_type == "product" and slug:
            product = get_object_or_404(Product, slug=slug, is_active=True)
            meta["title"] = f"{product.name} — купить в BAHO-MARKET по лучшей цене"
            meta["description"] = (product.description or product.name)[:160]
            meta["canonical"] = f"{domain}/product/{product.slug}"
            meta["og_title"] = meta["title"]
            meta["og_description"] = meta["description"]
            meta["hreflang"] = {
                "ru": f"{domain}/ru/product/{product.slug}",
                "uz": f"{domain}/uz/product/{product.slug}",
                "en": f"{domain}/en/product/{product.slug}",
            }
            if hasattr(product, "images") and product.images.exists():
                meta["og_image"] = product.images.first().image.url

            meta["json_ld"].append(JsonLdGenerator.get_product_schema(product))

            # Add Breadcrumbs Schema
            breadcrumbs = [
                {"name": "Главная", "url": "/"},
                {"name": product.category.name, "url": f"/category/{product.category.slug}"},
                {"name": product.name, "url": f"/product/{product.slug}"}
            ]
            meta["json_ld"].append(JsonLdGenerator.get_breadcrumb_schema(breadcrumbs))

        elif entity_type == "category" and slug:
            category = get_object_or_404(Category, slug=slug, is_active=True)
            meta["title"] = f"{category.name} — каталог товаров в BAHO-MARKET"
            meta["description"] = f"Купить {category.name} с гарантией и доставкой по Узбекистану."
            meta["canonical"] = f"{domain}/category/{category.slug}"
            meta["hreflang"] = {
                "ru": f"{domain}/ru/category/{category.slug}",
                "uz": f"{domain}/uz/category/{category.slug}",
                "en": f"{domain}/en/category/{category.slug}",
            }

        return Response(meta)
