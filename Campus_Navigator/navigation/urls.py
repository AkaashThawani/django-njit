from django.urls import path, include

from . import views

urlpatterns = [
    path('api/get_locations', views.get_locations, name='get_locations'),
    path('api/add_locations', views.add_location, name='add_location'),
    path('api/get_campus_events', views.CampusEventApiView.as_view(),
         name='get_campus_events'),
    path('api/get_buildings', views.get_buildings, name='get_buildings'),
    path('api/add_building', views.add_building, name='add_building'),
    path('api/get_feedback', views.get_buildings, name='get_buildings'),
    path('api/get_feedback_byID', views.add_building, name='add_building'),
    path('api/save_feedback', views.save_feedback, name='save_feedback'),
    path('api/login', views.user_login, name='login'),  # intigrated
    path('api/adminLogin', views.admin_login, name='adminlogin'),  # intigrated
    path('api/logout', views.user_logout, name='logout'),  # intigrated
    path('api/create-user', views.create_user,
         name='create_user'),  # intigrated
    path('api/create-admin', views.create_admin, name='create_admin'),
    path('api/validate-session', views.validate_user_session,
         name='validate_user_session'),

]
