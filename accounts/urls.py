from django.urls import path
from .import views
urlpatterns = [
    path('signup',views.signup_request , name="signup"),
    path('login',views.login_request , name="login"),
    path('logout',views.logout_request , name="logout"),
    path('profile/<slug:slug>',views.profile,name="profile"),
    path('settings',views.show_settings,name="settings"),
    path('addfriend',views.add_friend,name="addfriend"),
    path('deletefriend',views.delete_friend,name="deletefriend"),
    path('requestfriend',views.requestfriend,name="requestfriend"),
    path('searchfriend',views.search_friends,name="searchfriends"),
    path('changepass',views.change_pass,name="changepass"),
    
]