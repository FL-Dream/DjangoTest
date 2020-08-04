from django.urls import path
from booktest1 import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login),
    path('login_check', views.login_check),
    path('test_ajax', views.ajax_test),
    path('ajax_handle', views.ajax_handle),
    path('ajax_check', views.ajax_login),
    path('login1', views.login_ajax),
    path('set_cookie', views.set_cookie),
    path('get_cookie', views.get_cookie),
    path('set_session', views.set_session),
    path('get_session', views.get_session),
]