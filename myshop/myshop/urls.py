from django.conf.urls import include, url, static
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.login, {'extra_context': {'next':'/'}}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/logged_out/'}, name='logout'),
    url(r'^logout-then-login/$', views.logout_then_login, name='logout_then_login'),
    url(r'^', include('shop.urls', namespace='shop')),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        