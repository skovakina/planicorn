from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing, name='landing'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup, name='signup'),

    # Boards
    path('boards/create/', views.create_board, name='create_board'),
    path('boards/<int:board_id>/edit/', views.edit_board, name='edit_board'),
    path('boards/<int:board_id>/delete/', views.delete_board, name='delete_board'),
]