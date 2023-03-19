import shortner.views as views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<str:short_url>/', views.UrlRedirectView.as_view(), name='url_redirect'),
    path('api/<str:short_url>/', views.get_url, name='get_url'),
]
