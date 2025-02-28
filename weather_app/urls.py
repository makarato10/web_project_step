
from django.urls import path
from .views import home, register_view, login_view, logout_view, history_view

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('history/', history_view, name='history'),
]
