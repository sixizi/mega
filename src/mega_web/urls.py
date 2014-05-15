from django.conf.urls import patterns, include, url
from views import home,monitor,manage,resource,portal,fun
from views import instance,instance_add,instance_detail
from views import server,server_add,server_detail
from views import business,business_add,business_detail
from views import database,database_add,database_detail
from views import my_404_view,my_500_view
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#for error catch
handler404 = my_404_view
handler500 = my_500_view


urlpatterns = patterns('',
    url(r'^$',home),
    url(r'^resource/$',resource),
    url(r'^portal/$',portal),
    url(r'^monitor/$',monitor),
    url(r'^manage/$',manage),
    

#sub url
    url(r'^resource/instance/$',instance),
    url(r'^resource/instance_add/$',instance_add),
    url(r'^resource/instance_detail/$',instance_detail),
    
    url(r'^resource/server/$',server),
    url(r'^resource/server_add/$',server_add),
    url(r'^resource/server_detail/$',server_detail),

    url(r'^resource/business/$',business),
    url(r'^resource/business_add/$',business_add),
    url(r'^resource/business_detail/$',business_detail),

    url(r'^resource/database/$',database),
    url(r'^resource/database_add/$',database_add),
    url(r'^resource/database_detail/$',database_detail),

#for static like css ,js ,ima,music     
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_URL },name="static"),

#other
    url(r'^fun/$',fun),

)