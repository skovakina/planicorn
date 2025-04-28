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
    path('boards/<int:board_id>/', views.board_detail, name='board_detail'),

    # Events
    # Event routes
    path('boards/<int:board_id>/events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),

    # Tags
    path('boards/<int:board_id>/tags/create/', views.create_tag, name='create_tag'),
    path('tags/<int:tag_id>/delete/', views.delete_tag, name='delete_tag'),

]