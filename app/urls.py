from django.urls import path
from app import views
from .views import quiz_users, add_user, update_user, delete_user
from .views import manage_levels, add_level, update_level, delete_level
from .views import manage_questions, add_question, update_question, delete_question
from .views import manage_subjects, add_subject, update_subject, delete_subject, game_level, submit_quiz


urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('history', views.history, name='history'),
    
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    
    
    # path('level', views.level, name='level'),
    path('levels/', manage_levels, name='manage_levels'),
    path('levels/add/', add_level, name='add_level'),
    path('levels/update/<int:level_id>/', update_level, name='update_level'),
    path('levels/delete/<int:level_id>/', delete_level, name='delete_level'),
    
    
    path('questions/', manage_questions, name='manage_questions'),
    path('questions/add/', add_question, name='add_question'),
    path('questions/update/<int:question_id>/', update_question, name='update_question'),
    path('questions/delete/<int:question_id>/', delete_question, name='delete_question'),
    

    # path('quiz_users/', views.quiz_users, name='quiz_users'),
    # path('add_user/', views.add_user, name='add_user'),
    # path('update_user/', views.update_user, name='update_user'),
    path('quiz_users/', quiz_users, name='manage_users'),  # Updated to use quiz_users
    path('users/add/', add_user, name='add_user'),
    path('users/update/<int:user_id>/', update_user, name='update_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    
    
    path('subjects/', manage_subjects, name='manage_subjects'),
    path('subjects/add/', add_subject, name='add_subject'),
    path('subjects/update/<int:subject_id>/', update_subject, name='update_subject'),
    path('subjects/delete/<int:subject_id>/', delete_subject, name='delete_subject'),
    
    
    
    path('game_level/<str:subject_name>/', views.game_level, name='game_level'),
    path('game_start/<str:subject_name>/<str:level_name>/', views.game_start, name='game_start'),
    path('quiz/<str:subject_name>/<str:level_name>/submit/', submit_quiz, name='submit_quiz'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
]
