# home/urls.py
from django.urls import path
from home import views
from home.views import *

urlpatterns = [
    path("", views.home, name="home"),
    path("contact",views.contact, name ='contact'),
    path('about',views.about, name = 'about'),
    path("currency/<currency>",views.dashboard),
 path('test',views.check_updates, name = 'test'),
]
