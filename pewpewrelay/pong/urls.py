from django.urls import path

from . import views

urlpatterns = [
    path('1', views.index1),
    path('2', views.index2),
    path('left_up', views.move_left_up),
    path('left_down', views.move_left_down),
    path('right_up', views.move_right_up),
    path('right_down', views.move_right_down),
]
