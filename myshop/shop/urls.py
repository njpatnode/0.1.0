from django.conf.urls import url
from . import views
from . import analysis_controller_views

urlpatterns = [
    url(r'^get_train_pct/(?P<slider_id>[-\w]+)/$', views.get_train_pct, name='get_train_pct'),
    url(r'^get_dropdown_hist/(?P<dropdown_id>[-\w]+)/$', views.get_dropdown_hist, name='get_dropdown_hist'),
    # Generic Result Handler
    url(r'^ajax_handler/(?P<trigger_controller_id>[-\w]+)/$', analysis_controller_views.ajax_handler, name='ajax_handler'),
    url(r'^handle_heatmap/(?P<name>[-\w]+)/$', views.handle_heatmap, name='handle_heatmap'),
    url(r'^analysis_controller/(?P<analysis_controller_id>[-\w]+)/$', analysis_controller_views.analysis_controller_detail, name='analysis_controller_detail'),
    url(r'^analysis_detail/(?P<analysis_id>[-\w]+)/$', views.run_detail, name='analysis_detail'),
    url(r'^$', views.product_list, name='product_list'),
    url(r'^addrun/$', views.run_add, name='run_add'),
    url(r'^add/$', views.product_add, name='add'),
    url(r'^dataset/(?P<dataset_id>[-\w]+)/$', views.dataset_detail, name='dataset_detail'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    url(r'^dataview/(?P<dataview_id>[-\w]+)/$', views.dataview_detail, name='dataview_detail'),
]


