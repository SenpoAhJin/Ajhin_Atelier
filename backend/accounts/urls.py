from django.urls import path
from .views import RegisterView, CustomLoginView, CurrentUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path("me/", CurrentUserView.as_view()),

]
