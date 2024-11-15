import shortner.views as views
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # path('<str:short_url>/', views.UrlRedirectView.as_view(), name='url_redirect'),
    path('api/<str:short_url>/', views.get_url, name='get_url'),
    path('save_ip/' , views.save_ip),
    path('copy/' , views.copy_ip),
    path('your_ip/', views.IPChecker.as_view(), name='ipchecker'),
    path('feature-status/<str:feature_name>/', views.check_feature_status, name='feature_status'),

]
