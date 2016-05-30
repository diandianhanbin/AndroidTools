# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com

from django.conf.urls import url
from . import views
__author__ = "Sven_Weng"

urlpatterns = [
    url(r'^$', views.index, name='index'),

]
