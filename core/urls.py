from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


api_urlpatterns = [
    # API docs
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),

    # Apps
    path("", include("app.api.urls")),
]

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("docs"))),
    path("admin/", admin.site.urls),
    path("api/", include(api_urlpatterns), name="api")
]
