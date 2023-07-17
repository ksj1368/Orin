from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/', include('allauth.urls'), name='google_login'),
    path('logout/', views.logout_view, name='logout'),
    path('registerauth/', views.register_success, name='register_success'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
    path('recovery/id/', views.RecoveryIdView.as_view(), name='recovery_id'),
    path('recovery/id/find/', views.ajax_find_id_view, name='ajax_id'),
    path('recovery/pw/', views.RecoveryPwView.as_view(), name='recovery_pw'),
    path('recovery/pw/find/', views.ajax_find_pw_view, name='ajax_pw'),
    path('recovery/pw/auth/', views.auth_confirm_view, name='recovery_auth'),
    path('recovery/pw/reset/', views.auth_pw_reset_view, name='recovery_pw_reset'),
    path('myprofile/password/', views.password_edit_view, name='password_edit'),
    path('myprofile/', views.my_profile_view, name='my_profile'),
    path('myprofile/update/', views.my_profile_update_view, name='my_profile_update'),
    path('myprofile/delete/', views.my_profile_delete_view, name='my_profile_delete'),
    path('myprofile/subscribe/', views.subscribe_view, name='my_profile_subscribe'),
    path('myprofile/unsubscribe/', views.unsubscribe_view, name='my_profile_unsubscribe'),
]