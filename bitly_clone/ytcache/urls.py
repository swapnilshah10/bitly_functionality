
from django.urls import path
from .views import *

urlpatterns = [
    path('all', Allvideos.as_view(), name='allvideos'),
    path('shorts', Shorts.as_view(), name='shorts'),
    path('tdm', Tdm.as_view(), name='tdm'),
    path('drills', Drills.as_view(), name='drills'),
    path('chess' , Chess.as_view(), name='chess'),
]
