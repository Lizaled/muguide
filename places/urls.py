from django.urls import path
from . import views

urlpatterns = [
    path('check-username/', views.check_username, name='check_username'),
    path('check-email/', views.check_email, name='check_email'),

    path('', views.places, name='places'),  # Главная страница приложения 
    path('<int:place_id>/', views.place_detail, name='place_detail'),
    path('<int:place_id>/add_review/', views.add_review, name='add_review'),

    path('search/', views.search_places, name='search_places'),  # Новый маршрут для поиска

    path('profile/delete/', views.delete_account, name='delete_account'),

    path('<int:place_id>/delete_review/<int:review_id>/', views.delete_review, name='delete_review'),

    
]


