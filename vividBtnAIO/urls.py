"""vividBtnAIO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path

from vividBtn import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^add-voice$', views.add_voice_data),
    re_path(r'^get-voice$', views.get_voice),
    re_path(r'^add-vtuber$', views.add_vtuber),
    re_path(r'^add-group$', views.add_group),
    re_path(r'^count$', views.item_click),
    # 请不要在生产环境打开本功能
    re_path(r'^del-all$', views.del_all),
]
