from django.contrib import admin
from django.urls import path
from newsapi_app.views import get_news_info_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get_news_info/', get_news_info_api, name='get_news_info_api'),
]
