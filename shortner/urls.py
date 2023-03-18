import shortner.views as views
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<str:short_url>/', views.UrlRedirectView.as_view(), name='url_redirect'),
]
