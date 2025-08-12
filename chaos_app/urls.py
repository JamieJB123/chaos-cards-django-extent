# filepath: chaos_app/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my-cards/', views.user_cards_view, name='user_cards'),
    path('my-cards/edit_card/<int:card_id>/', views.edit_card_view, name='edit_card'),
    path('my-cards/delete-card/<int:card_id>/', views.delete_card_view, name='delete-card'),
    path('spin/', views.random_card_view, name='spin_card'),
]
