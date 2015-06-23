# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from ninformes import settings
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ninformes.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('escolar.urls', namespace = "escolar")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
)
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = settings.SITE_NAME
admin.site.site_title = "Administración del " + settings.SITE_NAME
