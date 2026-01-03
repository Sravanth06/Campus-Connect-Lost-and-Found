from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('report/', views.report_item, name='report_item'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='items/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Edit & Delete URLs
    path('item/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('item/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('item/<int:item_id>/update/', views.update_item, name='update_item'),

    # NEW: AI Match Detail View
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
]