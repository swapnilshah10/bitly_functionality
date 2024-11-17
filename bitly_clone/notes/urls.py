from django.urls import path
from .views import *

urlpatterns = [
    path('create_user/' , create_user , name="create_user"),
    path('user_exists/' , userExists , name="userExists"),
    path('save_note/', save_note, name='save_note'),
    path('retrieve_notes/', retrieve_notes, name='retrieve_notes'),
    path('edit_note/<int:note_id>/', edit_note, name='edit_note'),    
]