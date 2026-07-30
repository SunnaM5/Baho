from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.seo.views import RobotsTxtView, DynamicSitemapXmlView

urlpatterns = [
    path("health/", include("apps.core.urls")),
    path("robots.txt", RobotsTxtView.as_view(), name="robots-txt"),
    path("sitemap.xml", DynamicSitemapXmlView.as_view(), name="sitemap-xml"),
    path("admin/", admin.site.urls),
    path("api/v1/seo/", include("apps.seo.urls")),
    path("api/v1/interactions/", include("apps.interactions.urls")),
    path("api/v1/cms/", include("apps.cms.urls")),
    path("api/v1/search/", include("apps.search.urls")),
    path("api/v1/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.categories.urls")),
    path("api/v1/", include("apps.brands.urls")),
    path("api/v1/", include("apps.orders.urls")),
    path("api/v1/", include("apps.reviews.urls")),
    path("api/v1/", include("apps.tradein.urls")),
    path("api/v1/", include("apps.cart.urls")),
    path("api/v1/", include("apps.favorites.urls")),
    path("api/v1/", include("apps.products.urls")),
    path("api/v1/core/", include("apps.core.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
