from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.cms.models import (
    SiteSettings,
    HeroSlide,
    HomeSectionLayout,
    ProductCollection,
    FAQItem,
    NewsArticle,
    AdvantageItem
)


class EnterpriseCMSTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.settings = SiteSettings.objects.create(
            site_name="BAHO MARKET TEST",
            phone_primary="+998901234567",
            email="support@baho.uz"
        )
        self.slide = HeroSlide.objects.create(
            title_ru="Скидки до 50%",
            title_uz="50% gacha chegirmalar",
            title_en="Up to 50% Off",
            desktop_image="cms/hero/test.jpg",
            priority=1
        )
        self.layout = HomeSectionLayout.objects.create(
            section_key="hero",
            title_ru="Баннеры",
            order=1,
            is_visible=True
        )
        self.faq = FAQItem.objects.create(
            question_ru="Как оформить заказ?",
            question_uz="Buyurtmani qanday joylashtirish kerak?",
            answer_ru="Выберите товар и нажмите Оформить",
            order=1
        )
        self.news = NewsArticle.objects.create(
            title_ru="Открытие нового филиала",
            slug="new-branch-opening",
            content_ru="Мы открылись в Ташкенте!",
            cover_image="cms/news/cover.jpg",
            published_at=timezone.now()
        )

    def test_homepage_unified_endpoint(self):
        response = self.client.get("/api/v1/cms/home/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("settings", response.data)
        self.assertIn("hero_slides", response.data)
        self.assertIn("layout_sections", response.data)
        self.assertEqual(response.data["settings"]["site_name"], "BAHO MARKET TEST")
        self.assertEqual(len(response.data["hero_slides"]), 1)

    def test_faq_list_endpoint(self):
        response = self.client.get("/api/v1/cms/faq/?lang=uz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"][0]["question"], "Buyurtmani qanday joylashtirish kerak?")

    def test_news_article_detail_endpoint(self):
        response = self.client.get(f"/api/v1/cms/news/{self.news.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Открытие нового филиала")

    def test_cache_invalidation_on_model_update(self):
        # Initial request caches data
        res1 = self.client.get("/api/v1/cms/home/")
        self.assertEqual(res1.data["settings"]["site_name"], "BAHO MARKET TEST")

        # Update SiteSettings
        self.settings.site_name = "UPDATED BAHO MARKET"
        self.settings.save()

        # Next request must reflect updated cache
        res2 = self.client.get("/api/v1/cms/home/")
        self.assertEqual(res2.data["settings"]["site_name"], "UPDATED BAHO MARKET")

    def test_auto_slug_generation(self):
        article = NewsArticle.objects.create(
            title_ru="Тестовая Статья Без Слага",
            content_ru="Содержимое",
            cover_image="cms/news/test.jpg",
            published_at=timezone.now()
        )
        self.assertTrue(article.slug)
        self.assertTrue(article.slug.startswith("article-"))
