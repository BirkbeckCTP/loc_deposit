from django.conf.urls import url

from plugins.loc_transporter import views


urlpatterns = [
    url(r'^manager/$', views.manager, name='loc_transporter_manager'),

    url(r'^manager/srn/add/$', views.manage_srn, name='loc_add_srn'),
    url(r'^manager/srn/(?P<srn_id>\d+)/edit/$', views.manage_srn, name='loc_edit_srn'),

    url(r'^manager/srn/(?P<srn_id>\d+)/issues/$', views.view_journal_issues, name='loc_view_journal_issues'),
]
