from django.urls import path
from authz.views import SignUpView, loginview, logoutview

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', loginview, name='login'),
    path('logout/', logoutview, name='logout'),
]
