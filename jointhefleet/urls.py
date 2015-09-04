from django.conf.urls import patterns, include, url

from jointhefleet import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^view$', views.view_history, name='view_history'),
    # Manage Account
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    #url(r'^chgpasswd/$', views.chgpasswd, name='chgpasswd'),
    url(r'^chgpasswd$', 'django.contrib.auth.views.password_change', {'post_change_redirect' : '/jointhefleet/chgpasswd/done'}, name="password_change"), 
    url(r'^chgpasswd/done$', 'django.contrib.auth.views.password_change_done'),
    url(r'^join/(\w+)', views.join_operation, name='join_operation'),
    url(r'^create$', views.create_operation, name='create_operation'),
    url(r'^(\d+)/edit', views.edit_operation, name='edit_operation'),
    url(r'^(\d+)/addkillmail', views.add_killmail, name='addkillmail_operation'),
    url(r'^(\d+)', views.view_operation, name='view_operation'),
    url(r'^(.*)$', views.not_found, name='not_found'),
)
