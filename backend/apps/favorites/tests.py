from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.categories.models import Category
from apps.brands.models import Brand
from apps.products.models import Product
from apps.favorites.models import Favorite

User = get_user_model()


class FavoriteTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number="+998909998877", password="password123")
        self.category = Category.objects.create(name="Часы", slug="watches")
        self.brand = Brand.objects.create(name="Apple", slug="apple")
        self.product = Product.objects.create(
            name="Apple Watch Series 9",
            slug="apple-watch-9",
            sku="AWS9-001",
            category=self.category,
            brand=self.brand,
            base_price=Decimal("4000000.00"),
            stock=10
        )

    def test_favorite_creation_and_unique_constraint(self):
        fav = Favorite.objects.create(user=self.user, product=self.product)
        self.assertEqual(Favorite.objects.filter(user=self.user).count(), 1)
        self.assertEqual(fav.product.name, "Apple Watch Series 9")
