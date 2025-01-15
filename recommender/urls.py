from django.urls import path
from  . import views


urlpatterns = [
    path("",views.index_view,name='home'),
    path("read/<str:pk>",views.read_course,name='read'),
    path('recommend/',views.recommend_view,name='recommend')
]