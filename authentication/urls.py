from django.urls import path, include
from users.views import login_view



urlpatterns = [
        path('login', login_view),
]