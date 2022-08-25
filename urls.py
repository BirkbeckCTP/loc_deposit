from django.conf.urls import url

from plugins.loc_deposit import views


urlpatterns = [
    url(r'^manager/$', views.manager, name='loc_deposit_manager'),

    url(r'^manager/srn/add/$', views.manage_srn, name='loc_add_srn'),
    url(r'^manager/srn/(?P<srn_id>\d+)/edit/$', views.manage_srn, name='loc_edit_srn'),
]
