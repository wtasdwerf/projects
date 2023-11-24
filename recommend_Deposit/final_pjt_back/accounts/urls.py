# from django.urls import path
# from . import views


# app_name = 'accounts'
# urlpatterns = [
#     path('login/', views.login, name='login'),
#     path('logout/', views.logout, name='logout'),
#     path('signup/', views.signup, name='signup'),
#     path('delete/', views.delete, name='delete'),
#     path('update/', views.update, name='update'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('user/add_cart/', views.add_cart),
    path('user/delete_cart/', views.delete_cart),
    path('user/<str:username>/', views.user_profile),
]

