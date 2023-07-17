from django.contrib import admin
from django.urls import path,include
from django.urls import re_path as url
from orin import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', views.index, name='index'), # '/' 에 해당되는 path
    path("allinonekt/", admin.site.urls),
    path("common/", include("common.urls")),
    path('orin/', include("orin.urls")),
    path("correction/", include('correction.urls')),
    path('board/', include('board.urls')),
    path('accounts/', include('allauth.urls')),
    path('about', views.about, name='about'),
    path('draft/', include('draft.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)