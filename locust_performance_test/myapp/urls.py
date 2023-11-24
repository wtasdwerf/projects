from django.urls import path, include
from . import views

urlpatterns = [
    path('A/', views.problem_a),
    path('B/', views.problem_b),
    path('C/', views.problem_c),
    path('D/', views.problem_d),
]