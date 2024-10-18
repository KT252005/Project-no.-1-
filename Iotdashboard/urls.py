from django.urls import path,include 
from . import views
from rest_framework import routers



urlpatterns = [
    path('', views.home, name='home'),
    path('connect/', views.connect_to_device, name='connect_to_device'),
    path('publish-form/',views.publish_form,name='publish_message_to_esp'),
    path('publish-form/publish/',views.publish_control_command,name='publishapi'),
    path('iotdashboard/tracking/',views.tracking,name="tracking"),
    path("live_tracking/",views.livetracking,name="livetracking"),
    path("publish-form/livetracking",views.livetracking,name="livetrack"),
    path("message",views.get_latest_message,name="get-latest-message"),
    
    
]