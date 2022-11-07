from django.urls import re_path

from plugins.loc_deposit import views


urlpatterns = [
    re_path(r'^manager/$', views.manager, name='loc_deposit_manager'),

    re_path(r'^manager/srn/add/$', views.manage_srn, name='loc_add_srn'),
    re_path(r'^manager/srn/(?P<srn_id>\d+)/edit/$', views.manage_srn, name='loc_edit_srn'),
]
