from django.urls import re_path, include
from .views import (
    login,
    signup,
    test_token,
    google,
    logout
    )



urlpatterns = [
    re_path('login', login, ),
    re_path('signup', signup, ),
    re_path('test_token', test_token, ),
    re_path('google', google ),
    re_path('logout', logout ),
]
