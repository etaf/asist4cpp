from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^stlist$', views.index, name='stlist'),
        url(r'^upload_student_list/$', views.upload_student_list,  name='upload_student_list'),
        url(r'^download_norm2rand/$', views.download_norm2rand, name='download_norm2rand'),
        url(r'^monitor/$', views.monitor, name='monitor'),
        url(r'^collect/$', views.collect, name='collect'),
        url(r'^start_collect/$', views.start_collect, name='start_collect'),
        url(r'^generate_norm2rand/$', views.generate_norm2rand, name='generate_norm2rand'),
        url(r'^download_result/$', views.download_result, name='download_result'),
        url(r'^update_monitor_table/$', views.update_monitor_table, name='update_monitor_table'),
        url(r'^switch_monitor/$', views.switch_monitor, name='switch_monitor'),
        url(r'^login/$', views.my_login, name='my_login'),
        url(r'^logout/$', views.my_logout, name='my_logout'),
        ]

