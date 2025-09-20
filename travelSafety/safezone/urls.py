from django.urls import path
from . import views

urlpatterns = [
    path("", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),   #login page
    path("user/dashboard/", views.user_dashboard, name="user_dashboard"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),
    path("emergency/", views.send_emergency, name="send_emergency"),
    path("police/dashboard/", views.police_dashboard, name="police_dashboard"),

] 
