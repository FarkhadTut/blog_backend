from django.urls import re_path, include
from .views import (
    LoginView,
    Signup,
    Google,
    LogoutView,
    UserView,
    CsrfTokenView
    )



urlpatterns = [
    re_path('login', LoginView.as_view(), name='login'),
    re_path('signup', Signup.as_view(), name='signup'),
    re_path('google', Google.as_view(), name='google'),
    re_path('logout', LogoutView.as_view(), name='logout'),
    re_path('account', UserView.as_view(), name='account'),
    re_path('set-csrf-token', CsrfTokenView.as_view(), name='csrf'),
]
