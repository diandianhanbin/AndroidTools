# ecoding=utf-8
from django.conf.urls import url
from . import views
__author__ = "Sven_Weng"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^lists/', views.lists, name='list'),
    url(r'^setuptools/', views.setuptools, name='setuptools'),
    url(r'^getmemdata/(?P<filename>\S+)/$', views.getMemData, name='getMemData'),
    url(r'^getdirlist/(?P<cate>\S+)/$', views.getDirList, name='getDirList'),
    url(r'^meminfo/', views.mem_info, name='mem_info'),
    url(r'^cpuinfo/', views.cpu_info, name='cpu_info'),
    url(r'^getcpudata/(?P<filename>\S+)/$', views.getCpuData, name='getCpuData'),
    url(r'^flow/', views.flowinfo, name='getFlow'),
    url(r'^flowinfo/(?P<filename>\S+)/$', views.getFlowInfo, name='getFlowInfo'),
    url(r'^testflow/', views.flowTest, name='flowTest'),
    url(r'^get_cur_packagename', views.get_cur_pknm, name='getCurPackagename'),
    url(r'^get_third_packagename', views.get_third_pknm, name='getThirdPackagename'),
]
