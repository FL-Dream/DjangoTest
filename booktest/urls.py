from django.urls import path, re_path
from booktest import views

urlpatterns = [
    path('index/', views.index, name='index'),
    # 没有Django1中URL的匹配问题
    path('index2/', views.index2, name='index2'),

    path('', views.show_books),
    path('<int:bid>', views.detail),
    path('delete/<int:bid>', views.delete),
    path('add', views.add),
    path('temp_var', views.temp_var),
    path('temp_tags', views.temp_tags),
    path('temp_filter', views.temp_filter),  # 模板过滤器
    path('temp_inherit', views.temp_inherit), # 模板继承
    path('html_escape', views.html_escape), # HTML转义

    path('index3', views.index3),  #获取IP地址
    path('show_upload', views.show_upload),
    path('upload_handle', views.uplaod_handle),
    path('showbook2', views.show_book2),
    re_path(r'^show_areas(?P<page>\d*)$', views.show_area),
    path('areas', views.area, name='省市县联动'),
    path('prov', views.prov, name='获取省级地区信息'),
    path('city<int:pid>', views.city, name='获取市级地区信息'),
    path('dis<int:cid>', views.dis, name='获取县级地区信息')
]
