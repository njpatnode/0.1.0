from django.conf.urls import url
from . import views

urlpatterns = [
 url(r'^$', views.product_list, name='product_list'),
    url(r'^addrun/$', views.run_add, name='run_add'),
    url(r'^add/$', views.product_add, name='add'),
   url(r'^dataset/(?P<name>[-\w]+)/$', views.dataset_detail, name='dataset_detail'),
 url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
 url(r'^dataview/(?P<name>[-\w]+)/$', views.dataview_detail, name='dataview_detail'),
 url(r'^run/(?P<name>[-\w]+)/$', views.run_detail, name='run_detail'),
]
