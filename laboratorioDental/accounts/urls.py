from django.urls import path
from .views import LoginView, CreateUserView, AppSingletonView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('app-singleton/', AppSingletonView.as_view(), name='app_singleton'),
]
