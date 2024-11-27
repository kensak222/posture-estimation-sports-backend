"""
URL configuration for posture_estimation_sports_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static

from posture_estimation.views import (
    HomePageView,
    ProcessVideoView,
)
from posture_estimation_sports_backend import settings

urlpatterns = [
    path("process-video/", ProcessVideoView.as_view(), name="process_video"),
    path(
        "", HomePageView.as_view(), name="home"
    ),  # '/' にアクセスした際に表示するページ
]

# MEDIA_URL配下のリクエストを処理
if settings.DEBUG:  # 開発時のみ有効
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
