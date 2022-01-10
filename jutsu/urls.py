"""Grimorio_T20 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import path
from . import views

app_name = 'jutsu'

urlpatterns = [
    path('', views.jutsus_page, name='jutsus_page'),
#     path('copysortingname/', views.copy_sorting_name, name='copy_sorting_name'),
#     path('removechar/', views.remove_strange_char, name='remove_strange_char'),
#     path('complete_fields/', views.complete_fields, name='complete_fields'),
#     path('trim/', views.trim, name='trim'),
    path('<int:jutsu_id>/', views.jutsu_details, name='jutsu_details'),
]
