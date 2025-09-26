from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    path('<int:id>/hide/', views.hide_movie, name='movies.hide_movie'),
    path('<int:id>/unhide/', views.unhide_movie, name='movies.unhide_movie'),
    path('hidden/', views.hidden_movies, name='movies.hidden_movies'),
    path('petitions/', views.petitions, name='movies.petitions'),
    path('petitions/create/', views.create_petition, name='movies.create_petition'),
    path('petitions/<int:pk>/', views.petition, name='movies.petition'),
]