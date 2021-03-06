"""ping_pong URL Configuration

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
from django.contrib import admin
from django.urls import path
from pp_score.views import *
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include



session_router = DefaultRouter()
session_router.register(r'', SessionViewset, basename='session')

game_router = DefaultRouter()
game_router.register(r'', GameViewset, basename='game')

get_score = ScoreViewset.as_view({'get': 'get_score'})
get_graph_data = ScoreViewset.as_view({'get': 'get_graph_data'})

get_current_session = ScoreInputViewSet.as_view({'get': 'get_current_session'})

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^session/', include(session_router.urls)),
    url(r'^game/', include(game_router.urls)),
    path('get_score/', get_score, name='get_score' ),
    path('get_graph_data/', get_graph_data, name='get_graph_data' ),
    path('get_current_session/', get_current_session, name='get_current_session' ),
]
