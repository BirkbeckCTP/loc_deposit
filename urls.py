from django.urls import re_path

from plugins.loc_transporter import views


urlpatterns = [
    re_path(r'^manager/$', views.manager, name='loc_transporter_manager'),
    re_path(r'^manager/srn/add/$', views.manage_srn, name='loc_add_srn'),
    re_path(
        r'^manager/srn/(?P<srn_id>\d+)/edit/$',
        views.manage_srn,
        name='loc_edit_srn',
    ),
    re_path(
        r'^manager/srn/(?P<srn_id>\d+)/issues/$',
        views.view_journal_issues,
        name='loc_view_journal_issues',
    ),
]
